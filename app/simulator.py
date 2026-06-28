import random
import time
from datetime import datetime
VEHICLE_IDS = ["TRK-001", "TRK-002", "TRK-003"]
NORMAL_RANGES = {
    "speed_kmh":        (0, 80),
    "engine_temp_c":    (70, 95),
    "oil_pressure_bar": (2.0, 4.5),
    "fuel_level_pct":   (20, 100),
    "battery_voltage_v": (12.0, 14.8)
}
def generate_reading(vehicle_id):
    return {
        "vehicle_id": vehicle_id,
        "timestamp": datetime.now().isoformat(),
        "speed_kmh": round(random.uniform(0, 120), 2),
        "engine_temp_c": round(random.uniform(60, 110), 2),
        "oil_pressure_bar": round(random.uniform(1.0, 5.0), 2),
        "fuel_level_pct": round(random.uniform(5, 100), 2),
        "battery_voltage_v": round(random.uniform(11.0, 15.5), 2)
    }
def run_simulator():
    print("Starting EcoSync-Edge Telemetry Simulator...")
    print("Press Ctrl+C to stop\n")
    
    while True:
        for vehicle_id in VEHICLE_IDS:
            reading = generate_reading(vehicle_id)
            print(f"[{reading['timestamp']}] {vehicle_id} | "
                  f"Speed: {reading['speed_kmh']} kmh | "
                  f"Temp: {reading['engine_temp_c']}°C | "
                  f"Oil: {reading['oil_pressure_bar']} bar | "
                  f"Fuel: {reading['fuel_level_pct']}% | "
                  f"Battery: {reading['battery_voltage_v']}V")
        
        time.sleep(2)
if __name__ == "__main__":
    run_simulator()