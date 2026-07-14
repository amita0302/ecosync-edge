from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.edge_filter import apply_edge_filter
from app.alert_engine import generate_alerts, get_all_alerts
from app.ml.anomaly import store_reading, detect_anomaly
from app.rag.rag_engine import generate_recommendation
load_dotenv()

from pydantic import BaseModel

class TelemetryReading(BaseModel):
    vehicle_id: str
    timestamp: str
    speed_kmh: float
    engine_temp_c: float
    oil_pressure_bar: float
    fuel_level_pct: float
    battery_voltage_v: float

app = FastAPI(
    title="EcoSync-Edge API",
    description="Intelligent Edge-Computing Pipeline for IoT Data Minimisation and Predictive Asset Analytics",
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_dashboard():
    return FileResponse("frontend/index.html")
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "project": "EcoSync-Edge",
        "version": "1.0.0"
    }
@app.post("/telemetry")
def receive_telemetry(reading: TelemetryReading):
    result = apply_edge_filter(reading.model_dump())
    store_reading(reading.model_dump())
    
    if result["mode"] == "CRITICAL":
        alerts = generate_alerts(reading.vehicle_id, result["violations"])
        result["alerts"] = alerts
    else:
        result["alerts"] = []
    
    return result

@app.get("/alerts")
def get_alerts():
    return {
        "total": len(get_all_alerts()),
        "alerts": get_all_alerts()
    }
@app.get("/predict/{vehicle_id}")
def predict_anomaly(vehicle_id: str):
    return detect_anomaly(vehicle_id) 

@app.post("/ai-recommendation")
def get_ai_recommendation(data: dict):
    return generate_recommendation(
        vehicle_id=data.get("vehicle_id"),
        alert_title=data.get("alert_title"),
        alert_message=data.get("alert_message"),
        parameter=data.get("parameter"),
        value=data.get("value")
    )      