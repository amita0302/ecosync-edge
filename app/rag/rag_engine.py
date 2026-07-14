import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

from app.rag.vectorstore import retrieve_docs

# Load environment variables
load_dotenv()

# Gemini model (Free tier supported)
GEMINI_MODEL = "gemini-3.5-flash"

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_recommendation(
    vehicle_id: str,
    alert_title: str,
    alert_message: str,
    parameter: str,
    value: float,
) -> dict:

    # Build search query
    query = (
        f"{alert_title}. {alert_message}. "
        f"Parameter: {parameter}, Value: {value}"
    )

    # Retrieve relevant maintenance documents
    retrieved_docs = retrieve_docs(query, top_k=2)

    if not retrieved_docs:
        return {
            "vehicle_id": vehicle_id,
            "alert_title": alert_title,
            "recommendation": "No relevant maintenance documentation found.",
            "retrieved_docs": [],
            "status": "no_docs_found",
        }

    # Build context
    context = ""

    for doc in retrieved_docs:
        context += f"\n\n### {doc['title']}\n{doc['content']}"

    prompt = f"""
You are an expert fleet maintenance advisor for commercial vehicles.

A critical alert has been triggered.

Vehicle ID: {vehicle_id}

Alert:
{alert_title}

Details:
{alert_message}

Sensor Parameter:
{parameter}

Current Value:
{value}

Maintenance Documentation:
{context}

Provide:

1. Severity (Low / Medium / High / Critical)
2. Immediate actions for the driver
3. Required service actions
4. Estimated urgency
5. Whether the vehicle should continue operating

Keep the answer under 200 words.
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        return {
            "vehicle_id": vehicle_id,
            "alert_title": alert_title,
            "parameter": parameter,
            "current_value": value,
            "recommendation": response.text,
            "retrieved_docs": [
                {
                    "title": doc["title"],
                    "similarity_score": doc["similarity_score"],
                }
                for doc in retrieved_docs
            ],
            "model_used": GEMINI_MODEL,
            "status": "success",
        }

    except ClientError as e:
        return {
            "vehicle_id": vehicle_id,
            "alert_title": alert_title,
            "parameter": parameter,
            "current_value": value,
            "recommendation": None,
            "retrieved_docs": [],
            "model_used": GEMINI_MODEL,
            "status": "api_error",
            "error": str(e),
        }

    except Exception as e:
        return {
            "vehicle_id": vehicle_id,
            "alert_title": alert_title,
            "parameter": parameter,
            "current_value": value,
            "recommendation": None,
            "retrieved_docs": [],
            "model_used": GEMINI_MODEL,
            "status": "error",
            "error": str(e),
        }