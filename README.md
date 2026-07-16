# 🌿 EcoSync-Edge
### Intelligent Edge-Computing Pipeline for IoT Data Minimisation and Predictive Asset Analytics

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9.0-orange?logo=scikit-learn)](https://scikit-learn.org)
[![FAISS](https://img.shields.io/badge/FAISS-1.14.3-blue)](https://github.com/facebookresearch/faiss)
[![Gemini](https://img.shields.io/badge/Gemini-2.0--flash--lite-purple?logo=google)](https://ai.google.dev)
[![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render)](https://ecosync-edge.onrender.com)

> **Live Demo:** [https://ecosync-edge.onrender.com](https://ecosync-edge.onrender.com)
> 
> **Built as part of HCLtech Open Innovation Learning Program Internship (June–July 2026)**

---

## 📌 Problem Statement

Modern connected commercial vehicles (trucks, industrial machines, smart grid sensors) generate high-frequency telemetry data every second. Streaming all this data to the cloud causes:

- **Massive bandwidth waste** — 70–80% of data is redundant "normal" readings
- **Inflated storage costs** — cloud databases flooded with repetitive idle-state data
- **Delayed anomaly detection** — critical signals buried in data noise

## 💡 Solution

EcoSync-Edge is an **Intelligent Edge-Filtering Pipeline** that runs smart compression logic at the source. It dynamically switches between:

- **ECO MODE** — low-frequency transmission when all parameters are normal (saves bandwidth)
- **CRITICAL MODE** — high-frequency real-time stream when anomalies are detected (protects uptime)

Additionally, it integrates a **RAG Pipeline** for AI-powered maintenance recommendations backed by a vehicle technical knowledge base.

---

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS Dashboard)
        │
        ▼
FastAPI Backend (Python)
        │
 ┌──────┼──────────────┬───────────────┐
 │      │              │               │
 ▼      ▼              ▼               ▼
Edge   Alert        ML Anomaly      RAG Pipeline
Filter Engine       Detection       (FAISS + Gemini)
Logic  (Incident    (Isolation
(ECO/  Translation) Forest)
CRITICAL)
```

---

## ✨ Features

### 🔁 Dynamic Edge-to-Cloud Ingestion Engine
- Real-time threshold cross-validation across 5 sensor parameters simultaneously
- Eliminates data redundancy at the source — reduces cloud ingress by up to **70–80%**
- Rule-based ECO/CRITICAL mode switching with millisecond response time

### ⚠️ Automated Incident Logging & Diagnostic Translation
- Converts raw sensor violations into human-readable maintenance alerts
- Severity classification: CRITICAL / HIGH / MEDIUM
- Unique alert IDs with vehicle ID, timestamp, and parameter context

### 📊 Real-Time Dashboard
- Live telemetry feed with auto-refresh every 3 seconds
- Anomalous values highlighted in red directly in the table
- Alert feed with color-coded severity cards
- Mini bar charts for speed, engine temperature, and oil pressure trends
- Fleet status panel with per-vehicle ECO/CRITICAL indicators

### 🤖 ML Anomaly Detection
- Isolation Forest algorithm (unsupervised ML) on rolling telemetry history
- Detects subtle anomalies that don't cross fixed thresholds
- Returns anomaly score and binary classification per vehicle
- Trained on last 100 readings per vehicle (rolling window)

### 🧠 RAG Pipeline — AI-Powered Maintenance Recommendations
- **Knowledge Base:** 7 domain-specific vehicle maintenance documents
- **Vector Store:** FAISS (Facebook AI Similarity Search) with cosine similarity
- **Embedding Model:** `all-MiniLM-L6-v2` (sentence-transformers)
- **LLM:** Google Gemini 2.0 Flash Lite for generation
- Retrieves top-2 relevant maintenance docs per alert and generates precise, document-backed recommendations

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Python 3.11, FastAPI, Uvicorn, Pydantic |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | scikit-learn (Isolation Forest) |
| **RAG Pipeline** | sentence-transformers, FAISS, Google Gemini API |
| **Database** | PostgreSQL (via SQLAlchemy + psycopg2) |
| **Deployment** | Render |
| **Version Control** | Git, GitHub |

---

## 🚗 Simulated Fleet

| Vehicle | Parameters Monitored |
|---------|---------------------|
| TRK-001 | Speed, Engine Temp, Oil Pressure, Fuel Level, Battery Voltage |
| TRK-002 | Speed, Engine Temp, Oil Pressure, Fuel Level, Battery Voltage |
| TRK-003 | Speed, Engine Temp, Oil Pressure, Fuel Level, Battery Voltage |

### Normal Operating Ranges (Thresholds)

| Parameter | Min | Max |
|-----------|-----|-----|
| Speed | 0 kmh | 80 kmh |
| Engine Temperature | 70°C | 95°C |
| Oil Pressure | 2.0 bar | 4.5 bar |
| Fuel Level | 20% | 100% |
| Battery Voltage | 12.0V | 14.8V |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Live dashboard |
| `GET` | `/health` | Server health check |
| `POST` | `/telemetry` | Receive and filter telemetry reading |
| `GET` | `/alerts` | Retrieve all generated alerts |
| `GET` | `/predict/{vehicle_id}` | ML anomaly detection for a vehicle |
| `POST` | `/ai-recommendation` | RAG-powered maintenance recommendation |

**Swagger UI:** `https://ecosync-edge.onrender.com/docs`

---

## 🧠 RAG Pipeline — How It Works

```
CRITICAL Alert Triggered
        │
        ▼
Build Search Query from Alert Context
        │
        ▼
Encode Query → Vector (sentence-transformers)
        │
        ▼
FAISS Similarity Search → Top-2 Maintenance Docs
        │
        ▼
Build Prompt: Alert + Retrieved Context
        │
        ▼
Gemini API → AI-Generated Maintenance Recommendation
        │
        ▼
Return: Recommendation + Source Docs + Similarity Scores
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/amita0302/ecosync-edge.git
cd ecosync-edge

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Run the Application

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

**Swagger UI:** `http://127.0.0.1:8000/docs`

---

## 📁 Project Structure

```
ecosync-edge/
├── app/
│   ├── main.py              # FastAPI entry point + all endpoints
│   ├── simulator.py         # IoT telemetry data generator
│   ├── edge_filter.py       # ECO/CRITICAL mode switching logic
│   ├── alert_engine.py      # Incident translation + alert generation
│   ├── ml/
│   │   └── anomaly.py       # Isolation Forest anomaly detection
│   ├── rag/
│   │   ├── knowledge_base.py  # Vehicle maintenance documents
│   │   ├── vectorstore.py     # FAISS vector store + retrieval
│   │   └── rag_engine.py      # RAG pipeline + Gemini generation
│   ├── models/
│   │   └── schemas.py       # Pydantic data models
│   └── db/
│       ├── database.py      # PostgreSQL connection
│       └── crud.py          # Database operations
├── frontend/
│   ├── index.html           # Dashboard UI
│   ├── style.css            # Styling
│   └── app.js               # Frontend logic + API integration
├── requirements.txt
├── render.yaml              # Render deployment config
└── .env                     # Environment variables (gitignored)
```

---

## 📈 Real-World Impact

| Metric | Value |
|--------|-------|
| Cloud data ingestion reduction | Up to 70–80% |
| Alert response time | < 1 second |
| Anomaly detection | Isolation Forest (unsupervised ML) |
| RAG knowledge base | 7 domain-specific maintenance documents |
| Vehicles monitored | 3 (scalable) |
| API endpoints | 6 |

---


---

## 📄 License

This project is licensed under the MIT License.
