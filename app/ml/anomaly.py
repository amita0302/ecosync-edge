import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime

# Stores recent readings per vehicle for ML training
vehicle_data_store = {
    "TRK-001": [],
    "TRK-002": [],
    "TRK-003": []
}

# Minimum readings needed before we can run anomaly detection
MIN_READINGS = 20

def store_reading(reading):
    vehicle_id = reading.get("vehicle_id")
    
    if vehicle_id not in vehicle_data_store:
        return
    
    vehicle_data_store[vehicle_id].append([
        reading.get("speed_kmh", 0),
        reading.get("engine_temp_c", 0),
        reading.get("oil_pressure_bar", 0),
        reading.get("fuel_level_pct", 0),
        reading.get("battery_voltage_v", 0)
    ])
    
    # Keep only last 100 readings per vehicle
    if len(vehicle_data_store[vehicle_id]) > 100:
        vehicle_data_store[vehicle_id] = vehicle_data_store[vehicle_id][-100:]


def detect_anomaly(vehicle_id):
    data = vehicle_data_store.get(vehicle_id, [])
    
    if len(data) < MIN_READINGS:
        return {
            "vehicle_id": vehicle_id,
            "status": "insufficient_data",
            "message": f"Need at least {MIN_READINGS} readings. Currently have {len(data)}.",
            "anomaly_score": None,
            "is_anomaly": False
        }
    
    X = np.array(data)
    
    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )
    
    model.fit(X)
    
    latest_reading = np.array([data[-1]])
    score = model.score_samples(latest_reading)[0]
    prediction = model.predict(latest_reading)[0]
    
    is_anomaly = bool(prediction == -1)
    
    return {
        "vehicle_id": vehicle_id,
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "anomaly_score": round(float(score), 4),
        "is_anomaly": is_anomaly,
        "message": "Anomaly detected — unusual pattern in telemetry data." if is_anomaly else "Normal operation detected."
    }