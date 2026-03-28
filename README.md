# 🏙️ AI Civic Intelligence System (Agentic AI Project)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gp9zcjdbzxeddof8sdhekc.streamlit.app/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)

## 🧠 Introduction
The **AI Civic Intelligence System** is an Agentic AI-based platform designed to automate the detection, reporting, and verification of civic infrastructure issues such as potholes, garbage accumulation, and road damage. 

The goal of this system is to reduce manual intervention, improve response time from authorities, and create a smart, automated civic monitoring solution using AI and intelligent workflows.

**Live Demo:** [Streamlit Deployment](https://gp9zcjdbzxeddof8sdhekc.streamlit.app/)

---

## 🎯 Problem Statement
In traditional systems:
* Civic issues are reported manually.
* There is no proper prioritization of critical infrastructure decay.
* Authorities experience delays in response and resolution.
* There is a distinct lack of verification after an issue is claimed to be resolved.

👉 **This project solves these problems using AI + Automation + Multi-Agent Workflows.**

---

## 💡 Core Idea
The system leverages a synergy of modern technologies:
* **Computer Vision (YOLO)** → To detect physical issues from images.
* **Agentic AI (LangGraph + MCP)** → To manage complex workflow decisions and state routing.
* **Automation (SendGrid)** → To notify the appropriate civic departments.
* **Verification Logic** → To programmatically confirm issue resolution.

---

## 🔍 Key Components Explained

### 1. 🧠 AI-Based Issue Detection
Uses a **YOLO (You Only Look Once)** object detection model to identify civic hazards like potholes, garbage, and road damage.
* **Outputs:** Bounding boxes, Confidence scores, and Detected class labels.

### 2. 🤖 Agentic AI Workflow (LangGraph + MCP)
*This is the core innovation of the project.* Instead of a rigid, linear pipeline, the system uses multiple intelligent agents:
* **Detection Agent:** Identifies the issue from the image payload.
* **Routing Agent:** Determines the correct municipal department to contact.
* **Priority Agent:** Assigns severity based on context.
* **Notification Agent:** Dispatches automated emails.
* **Verification Agent:** Checks post-repair images for resolution.

👉 These agents coordinate using **LangGraph** (for workflow orchestration) and **MCP** (Multi-agent Control Protocol for structured execution).

### 3. 📍 Location Extraction
The system extracts real-world coordinates using two fallback methods, ensuring location availability even without native GPS tracking:
* **EXIF Metadata:** Reads latitude & longitude directly from image properties.
* **OCR (Tesseract):** Extracts visible location text/signs from the image itself.

### 4. 🚦 Severity & Priority Classification
Assigns priority levels (**Low, Medium, High**) dynamically based on the detected bounding box area, AI confidence score, and specific issue type.

### 5. 📩 Automated Notification System
Integrates the **SendGrid API** to dispatch structured emails to departments containing the issue type, priority level, location coordinates, and annotated image evidence.

### 6. 🔄 Verification Pipeline & Image Comparison
Closes the loop on civic maintenance:
* An authority uploads a "resolved" repair image.
* The system retrieves the original issue and compares the two states.
* The AI verifies the resolution, ensuring accountability and transparency.

---

## 🛠️ Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Frontend** | Streamlit |
| **Backend API** | FastAPI, Python |
| **AI / ML** | YOLO, PyTorch |
| **Orchestration** | LangGraph, MCP |
| **Image Processing** | OpenCV (`opencv-python-headless`), Pillow |
| **OCR** | Tesseract |
| **Notifications** | SendGrid |
| **Database** | SQLite |

---

## 🚀 Deployment Architecture

This system utilizes a **Decoupled Microservice Architecture** to efficiently handle heavy machine-learning workloads without compromising frontend speed or user experience.

* **Backend API (Hugging Face Spaces):** * Hosted in a custom **Docker container** to provide the 16GB of RAM required for loading YOLO and PyTorch models into memory.
  * Runs the FastAPI server (`uvicorn`) and exposes the core inference and LangGraph endpoints (`/detect`, `/verify`).
  * Handles all OpenCV system dependencies (`libgl1`) via the Dockerfile.
* **Frontend UI (Streamlit Community Cloud):** * A lightweight, purely interactive web dashboard.
  * Communicates seamlessly with the Hugging Face FastAPI endpoints via RESTful HTTP requests, displaying real-time analytics, maps, and AI-annotated images to the user.

---

## 📂 Repository Structure

```text
├── backend/
│   ├── agents/            # AI agent logic (Routing, Priority, Notification, Verification)
│   ├── db/                # Database initialization and SQLite schemas
│   ├── graph/             # LangGraph state definitions and workflow orchestration
│   ├── mcp_tools/         # Multi-agent Control Protocol integrations
│   ├── model/             # YOLO model files and inference configurations
│   ├── runs/detect/       # YOLO inference outputs and saved visualizations
│   ├── tool/              # Helper tools (GPS extraction, image processing)
│   ├── uploads/           # Directory for storing uploaded civic issue images
│   ├── config.py          # Environment variables and configuration settings
│   ├── main.py            # FastAPI application and endpoints
│   ├── requirements.txt   # Backend dependencies (FastAPI, PyTorch, OpenCV, etc.)
│   ├── runtime.txt        # Python runtime specification for cloud deployment
│   └── test_detect.py     # Local testing script for object detection
│
├── frontend/
│   ├── app.py             # Streamlit dashboard and UI logic
│   └── requirements.txt   # Lightweight frontend dependencies (Streamlit, Requests)
│
└── README.md              # Project documentation
