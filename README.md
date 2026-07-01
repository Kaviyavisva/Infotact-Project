# Prescriptive Maintenance RAG Agent for HVAC Systems


## Project Overview

The Prescriptive Maintenance RAG Agent is an AI-based maintenance recommendation system for HVAC equipment.

The system uses IoT alerts, Retrieval Augmented Generation (RAG), vector search and recommendation logic to identify faults and provide maintenance actions.


# System Workflow


IoT Alert Generator

|

v

Alert Processing

|

v

Embedding Generation

|

v

ChromaDB Vector Retrieval

|

v

Recommendation Engine

|

v

Final Maintenance Report



# Project Modules


## 1. IoT Alert Module


File:

src/iot_alert.py


Responsibilities:

- Generates simulated HVAC sensor alerts
- Creates machine fault conditions
- Produces alerts.json



## 2. Document Processing


Files:

src/parser.py

src/chunker.py


Responsibilities:

- Extract maintenance manual information
- Split documents into chunks



## 3. Embedding Module


File:

src/embedder.py


Responsibilities:

- Converts document chunks into vector embeddings
- Uses Sentence Transformer model



## 4. Vector Database


Files:

src/vector_store.py

src/search_engine.py


Responsibilities:

- Stores document embeddings
- Performs similarity search using ChromaDB



## 5. Recommendation Engine


File:

src/recommendation_engine.py


Responsibilities:

- Analyzes retrieved maintenance information
- Generates corrective actions



## 6. RAG Pipeline


File:

src/rag_pipeline.py


Responsibilities:

Complete integration:


IoT Alert

|

v

Search Engine

|

v

Recommendation Engine

|

v

Final Maintenance Output



# Installation


Create virtual environment:


python -m venv venv


Activate environment:


Windows:

venv\Scripts\activate


Install dependencies:


pip install -r requirements.txt



# Running the Project


Generate IoT Alerts:


python src/iot_alert.py


Run complete RAG pipeline:


python src/rag_pipeline.py



# Testing


Run validation:


python src/test_rag_pipeline.py



# Example Input


Sensor:
Voltage Sensor


Error:
SHORT_CIRCUIT


Severity:
HIGH



# Example Output


The system generates:

- Fault analysis
- Maintenance recommendation
- Required tools
- Required parts
- Repair guidance



# Technologies Used


- Python
- ChromaDB
- Sentence Transformers
- Retrieval Augmented Generation (RAG)
- Artificial Intelligence
- IoT Simulation



# Week 4 Integration Role


Integration Coordinator:

Kaviyashri Viswanathan


Responsibilities:

- Complete RAG workflow integration
- Connected IoT Alert -> Search -> Recommendation pipeline
- Performed end-to-end testing
- Validated multiple fault scenarios
- Prepared documentation
- Prepared demonstration workflow