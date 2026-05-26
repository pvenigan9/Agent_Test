# 🤖 Agent_Test Repository

A comprehensive Python project exploring AI agents and LLM integrations with multiple implementations and tools.

## 📋 Project Overview

This repository contains various implementations of conversational AI agents using modern LLM frameworks (Google Gemini, OpenAI), FastAPI backends, and interactive Streamlit interfaces. Each module demonstrates different aspects of building intelligent agents with tool-calling capabilities.

---

## 📁 File Documentation

### **agent.py**
**Purpose**: Modern Gemini-based conversational agent with tool integration and Streamlit UI

**Key Features**:
- Built with LangChain v1.0 and Google Gemini 3.1 Flash
- Interactive Streamlit chat interface
- Tool calling system for real-time capabilities
- Session state management for chat history

**Main Components**:
- `get_system_time()`: Tool that returns current system time
- Agent initialization with Gemini 3.1 Flash model
- Chat message history tracking
- Status display showing agent's thought process

**Usage**:
```bash
streamlit run agent.py

----------
agenttools.py
Purpose: Advanced agent with multiple specialized tools for financial and real-time data

Key Features:

Multiple tool integrations (stock prices, gold prices, SEC EDGAR)
Streamlit chat interface with tool demonstrations
Real-world API integrations
Error handling and fallback responses
Tools Included:

get_system_time(): Returns current system time
get_stock_price(ticker): Fetches live stock prices using Yahoo Finance
get_edgar_api(company_name): Retrieves SEC EDGAR company filings
get_gold_price(query): Gets current gold prices with AED conversion
Usage:

bash
streamlit run agenttools.py

Requirements:

langchain_google_genai
langchain
streamlit
yfinance
requests
python-dotenv
---------
app.py
Purpose: FastAPI backend for metadata extraction and entity recognition

Key Features:

RESTful API endpoints for text processing
Regex-based metadata extraction
Structured response formatting
Production-ready FastAPI application
Endpoints:

POST /extract: Extracts metadata from raw text
Extracts: primary subject, dates, locations, mission keywords, technical terms
Returns: confidence score and structured metadata
GET /: Health check endpoint

Request Format:

JSON
{
  "raw_text": "Your text here"
}

Response Format:

JSON
{
  "confidence_score": 95,
  "extracted_metadata": {
    "primary_subject": "Project Apollo-11",
    "tags": ["Houston", "July 20, 1969", "lunar landing"],
    "technical_keywords": ["navigation", "telemetry systems"]
  }
}
Usage:

bash
uvicorn app:app --reload
Requirements:

fastapi
uvicorn
pydantic
