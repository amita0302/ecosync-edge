// EcoSync-Edge Dashboard — frontend logic
// Simulates telemetry (same ranges as backend simulator.py), POSTs each
// reading to /telemetry, and renders the live results + /alerts feed.

const API_BASE = "";
const VEHICLE_IDS = ["TRK-001", "TRK-002", "TRK-003"];
const REFRESH_MS = 3000;
const HISTORY_LEN = 12;

// Same generation ranges as backend/simulator.py
const GEN_RANGES = {
    speed_kmh: [0, 120],
    engine_temp_c: [60, 110],
    oil_pressure_bar: [1.0, 5.0],
    fuel_level_pct: [5, 100],
    battery_voltage_v: [11.0, 15.5]
};

// Same safe thresholds as backend/edge_filter.py (used only for bar coloring)
const THRESHOLDS = {
    speed_kmh: [0, 80],
    engine_temp_c: [70, 95],
    oil_pressure_bar: [2.0, 4.5],
    fuel_level_pct: [20, 100],
    battery_voltage_v: [12.0, 14.8]
};

// vehicle_id -> latest /telemetry response
const latestResults = {};

// rolling history per chart (fixed vehicle/metric pairing, as in the UI)
const history = {
    "TRK-001": { param: "speed_kmh", values: [] },
    "TRK-002": { param: "engine_temp_c", values: [] },
    "TRK-003": { param: "oil_pressure_bar", values: [] }
};

function randomInRange([min, max]) {
    return Math.round((Math.random() * (max - min) + min) * 100) / 100;
}

function generateReading(vehicleId) {
    return {
        vehicle_id: vehicleId,
        timestamp: new Date().toISOString(),
        speed_kmh: randomInRange(GEN_RANGES.speed_kmh),
        engine_temp_c: randomInRange(GEN_RANGES.engine_temp_c),
        oil_pressure_bar: randomInRange(GEN_RANGES.oil_pressure_bar),
        fuel_level_pct: randomInRange(GEN_RANGES.fuel_level_pct),
        battery_voltage_v: randomInRange(GEN_RANGES.battery_voltage_v)
    };
}

async function postTelemetry(reading) {
    const response = await fetch(`${API_BASE}/telemetry`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(reading)
    });
    if (!response.ok) {
        throw new Error(`Telemetry POST failed: ${response.status}`);
    }
    return response.json();
}

function isViolated(param, value) {
    const [min, max] = THRESHOLDS[param];
    return value < min || value > max;
}

function updateClock() {
    const el = document.getElementById("last-updated");
    const now = new Date();
    el.textContent = `${now.toLocaleTimeString()} · Refresh 3s`;
}

function updateTelemetryTable() {
    const tbody = document.getElementById("telemetry-body");
    tbody.innerHTML = "";

    VEHICLE_IDS.forEach(vehicleId => {
        const result = latestResults[vehicleId];
        if (!result) return;

        const reading = result.reading;
        const isCritical = result.mode === "CRITICAL";
        const violatedParams = new Set(result.violations.map(v => v.parameter));

        const cellClass = (param) => violatedParams.has(param) ? "danger" : "";

        const row = document.createElement("tr");
        row.innerHTML = `
            <td class="primary">${result.vehicle_id}</td>
            <td class="${cellClass("speed_kmh")}">${reading.speed_kmh}</td>
            <td class="${cellClass("engine_temp_c")}">${reading.engine_temp_c}</td>
            <td class="${cellClass("oil_pressure_bar")}">${reading.oil_pressure_bar}</td>
            <td class="${cellClass("fuel_level_pct")}">${reading.fuel_level_pct}</td>
            <td class="${cellClass("battery_voltage_v")}">${reading.battery_voltage_v}</td>
            <td><span class="mb ${isCritical ? "mb-crit" : "mb-eco"}">${result.mode}</span></td>
        `;
        tbody.appendChild(row);
    });
}

function updateFleetPanel() {
    const suffixMap = { "TRK-001": "trk1", "TRK-002": "trk2", "TRK-003": "trk3" };

    VEHICLE_IDS.forEach(vehicleId => {
        const result = latestResults[vehicleId];
        if (!result) return;

        const suffix = suffixMap[vehicleId];
        const dot = document.getElementById(`dot-${suffix}`);
        const chip = document.getElementById(`chip-${suffix}`);
        const isCritical = result.mode === "CRITICAL";

        dot.className = `fleet-dot ${isCritical ? "fd-crit" : "fd-eco"}`;
        chip.className = `fleet-chip ${isCritical ? "fc-crit" : "fc-eco"}`;
        chip.textContent = result.mode;
    });
}

function updateMetrics() {
    const results = Object.values(latestResults);
    const criticalCount = results.filter(r => r.mode === "CRITICAL").length;
    const ecoCount = results.length - criticalCount;

    document.getElementById("critical-count").textContent = criticalCount;
    document.getElementById("eco-count").textContent = ecoCount;

    const criticalSub = document.getElementById("critical-sub");
    if (criticalCount === 0) {
        criticalSub.textContent = "All clear";
    } else if (criticalCount === results.length) {
        criticalSub.textContent = "↑ All vehicles critical";
    } else {
        criticalSub.textContent = `↑ ${criticalCount} vehicle(s) critical`;
    }
}

function updateCharts() {
    const chartMeta = {
        "TRK-001": { valId: "chart-val-1", barsId: "bars-1", unit: "kmh", normalColor: "#cae8ff", dangerColor: "#ffcecb" },
        "TRK-002": { valId: "chart-val-2", barsId: "bars-2", unit: "°C", normalColor: "#fae17d", dangerColor: "#ffcecb" },
        "TRK-003": { valId: "chart-val-3", barsId: "bars-3", unit: "bar", normalColor: "#fae17d", dangerColor: "#ffcecb" }
    };

    VEHICLE_IDS.forEach(vehicleId => {
        const result = latestResults[vehicleId];
        if (!result) return;

        const { param, values } = history[vehicleId];
        const value = result.reading[param];

        values.push(value);
        if (values.length > HISTORY_LEN) values.shift();

        const meta = chartMeta[vehicleId];
        document.getElementById(meta.valId).textContent = `${value} ${meta.unit}`;

        const [genMin, genMax] = GEN_RANGES[param];
        const barsEl = document.getElementById(meta.barsId);
        barsEl.innerHTML = values.map(v => {
            const pct = Math.max(5, Math.min(100, ((v - genMin) / (genMax - genMin)) * 100));
            const color = isViolated(param, v) ? meta.dangerColor : meta.normalColor;
            return `<div class="b" style="height:${pct.toFixed(0)}%;background:${color}"></div>`;
        }).join("");
    });
}

function severityClasses(severity) {
    const map = {
        CRITICAL: { item: "ai-crit", title: "ait-crit", sev: "sev-crit" },
        HIGH: { item: "ai-high", title: "ait-high", sev: "sev-high" },
        MEDIUM: { item: "ai-med", title: "ait-med", sev: "sev-med" }
    };
    return map[severity] || map.MEDIUM;
}

async function updateAlerts() {
    try {
        const response = await fetch(`${API_BASE}/alerts`);
        if (!response.ok) throw new Error(`Alerts GET failed: ${response.status}`);
        const data = await response.json();

        document.getElementById("total-alerts").textContent = data.total;
        document.getElementById("alert-badge").textContent = data.total;

        const alertFeed = document.getElementById("alert-feed");

        if (data.alerts.length === 0) {
            alertFeed.innerHTML = '<p style="color:#8c959f;font-size:12px">No alerts yet...</p>';
            return;
        }

        const recentAlerts = data.alerts.slice(-10).reverse();

        alertFeed.innerHTML = recentAlerts.map(alert => {
            const cls = severityClasses(alert.severity);
            const time = new Date(alert.timestamp).toLocaleTimeString();
            return `
                <div class="alert-item ${cls.item}">
                    <div class="ai-head">
                        <span class="ai-title ${cls.title}">${alert.title}</span>
                        <span class="sev ${cls.sev}">${alert.severity}</span>
                    </div>
                    <div class="ai-msg">${alert.message}</div>
                    <div class="ai-foot"><span class="ai-meta">${alert.vehicle_id} · ${time}</span></div>
                </div>
            `;
        }).join("");
    } catch (err) {
        console.error("Failed to update alerts:", err);
    }
}

async function refreshCycle() {
    try {
        for (const vehicleId of VEHICLE_IDS) {
            const reading = generateReading(vehicleId);
            const result = await postTelemetry(reading);
            latestResults[vehicleId] = result;
        }

        updateClock();
        updateTelemetryTable();
        updateFleetPanel();
        updateMetrics();
        updateCharts();
        await updateAlerts();
    } catch (err) {
        console.error("Refresh cycle failed:", err);
    }
}

refreshCycle();
setInterval(refreshCycle, REFRESH_MS);