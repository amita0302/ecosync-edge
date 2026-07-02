from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.edge_filter import apply_edge_filter
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
    return result    