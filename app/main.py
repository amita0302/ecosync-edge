from fastapi import FastAPI
from dotenv import load_dotenv
import os
load_dotenv()

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