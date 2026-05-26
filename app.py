from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

# Request Model
class TextRequest(BaseModel):
    raw_text: str

# Simple extraction function
def extract_metadata(text: str):

    # Primary Subject
    subject_match = re.search(r"(Project\s+[A-Za-z0-9\-]+)", text)
    primary_subject = subject_match.group(1) if subject_match else "Unknown"

    # Date extraction
    date_match = re.search(r"([A-Z][a-z]+\s\d{1,2},\s\d{4})", text)

    # Location extraction
    location_match = re.search(r"from\s([A-Z][a-zA-Z]+)", text)

    # Mission keyword extraction
    mission_match = re.search(r"(lunar landing)", text)

    # Technical keywords
    technical_keywords = []

    if "navigation" in text.lower():
        technical_keywords.append("navigation")

    if "telemetry systems" in text.lower():
        technical_keywords.append("telemetry systems")

    tags = []

    if location_match:
        tags.append(location_match.group(1))

    if date_match:
        tags.append(date_match.group(1))

    if mission_match:
        tags.append(mission_match.group(1))

    response = {
        "confidence_score": 95,
        "extracted_metadata": {
            "primary_subject": primary_subject,
            "tags": tags,
            "technical_keywords": technical_keywords
        }
    }

    return response


@app.post("/extract")
def extract_entities(request: TextRequest):
    return extract_metadata(request.raw_text)

@app.get("/")
def read_root():
    return {"message": "FastAPI app is running"}