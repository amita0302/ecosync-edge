from datetime import datetime
THRESHOLDS = {
    "speed_kmh":         {"min": 0,    "max": 80},
    "engine_temp_c":     {"min": 70,   "max": 95},
    "oil_pressure_bar":  {"min": 2.0,  "max": 4.5},
    "fuel_level_pct":    {"min": 20,   "max": 100},
    "battery_voltage_v": {"min": 12.0, "max": 14.8}
}
def check_thresholds(reading):
    violations = []
    
    for parameter, limits in THRESHOLDS.items():
        value = reading.get(parameter)
        
        if value is None:
            continue
            
        if value < limits["min"] or value > limits["max"]:
            violations.append({
                "parameter": parameter,
                "value": value,
                "min": limits["min"],
                "max": limits["max"]
            })
    
    return violations
def apply_edge_filter(reading):
    violations = check_thresholds(reading)
    
    if violations:
        mode = "CRITICAL"
    else:
        mode = "ECO"
    
    return {
        "vehicle_id": reading.get("vehicle_id"),
        "timestamp": reading.get("timestamp"),
        "mode": mode,
        "violations": violations,
        "reading": reading
    }
if __name__ == "__main__":
    # Test 1 - Critical reading
    critical_reading = {
        "vehicle_id": "TRK-001",
        "timestamp": datetime.now().isoformat(),
        "speed_kmh": 95.0,
        "engine_temp_c": 105.0,
        "oil_pressure_bar": 3.0,
        "fuel_level_pct": 50.0,
        "battery_voltage_v": 13.5
    }
    
    # Test 2 - Normal reading
    normal_reading = {
        "vehicle_id": "TRK-002",
        "timestamp": datetime.now().isoformat(),
        "speed_kmh": 60.0,
        "engine_temp_c": 85.0,
        "oil_pressure_bar": 3.0,
        "fuel_level_pct": 50.0,
        "battery_voltage_v": 13.5
    }
    
    for reading in [critical_reading, normal_reading]:
        result = apply_edge_filter(reading)
        print(f"Vehicle: {result['vehicle_id']} | Mode: {result['mode']} | Violations: {result['violations']}")
        print()