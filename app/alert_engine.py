from datetime import datetime
ALERT_TEMPLATES = {
    "speed_kmh": {
        "title": "Overspeed Alert",
        "message": "Vehicle exceeding safe speed limit. Current: {value} kmh (limit: {max} kmh). Driver intervention required immediately.",
        "severity": "HIGH"
    },
    "engine_temp_c": {
        "title": "Engine Overheating",
        "message": "Engine temperature critical. Current: {value}°C (limit: {max}°C). Schedule coolant inspection within 24 hours.",
        "severity": "CRITICAL"
    },
    "oil_pressure_bar": {
        "title": "Oil Pressure Anomaly",
        "message": "Oil pressure out of safe range. Current: {value} bar (range: {min}-{max} bar). Inspect oil system before next trip.",
        "severity": "CRITICAL"
    },
    "fuel_level_pct": {
        "title": "Low Fuel Warning",
        "message": "Fuel level critically low. Current: {value}% (minimum: {min}%). Refuel at nearest station.",
        "severity": "MEDIUM"
    },
    "battery_voltage_v": {
        "title": "Battery Voltage Anomaly",
        "message": "Battery voltage out of range. Current: {value}V (range: {min}-{max}V). Inspect electrical system.",
        "severity": "HIGH"
    }
}
alert_store = []
def generate_alerts(vehicle_id, violations):
    alerts = []
    
    for violation in violations:
        parameter = violation["parameter"]
        template = ALERT_TEMPLATES.get(parameter)
        
        if template:
            alert = {
                "alert_id": f"{vehicle_id}-{parameter}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "vehicle_id": vehicle_id,
                "timestamp": datetime.now().isoformat(),
                "title": template["title"],
                "message": template["message"].format(
                    value=violation["value"],
                    min=violation["min"],
                    max=violation["max"]
                ),
                "severity": template["severity"],
                "parameter": parameter
            }
            alerts.append(alert)
            alert_store.append(alert)
    
    return alerts
def get_all_alerts():
    return alert_store
if __name__ == "__main__":
    test_violations = [
        {
            "parameter": "engine_temp_c",
            "value": 105.0,
            "min": 70,
            "max": 95
        },
        {
            "parameter": "speed_kmh",
            "value": 95.0,
            "min": 0,
            "max": 80
        }
    ]
    
    alerts = generate_alerts("TRK-001", test_violations)
    
    for alert in alerts:
        print(f"[{alert['severity']}] {alert['title']}")
        print(f"Message: {alert['message']}")
        print()