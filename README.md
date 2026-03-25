# 🚀 AI Civic Intelligence System (Agentic AI Project)

## 🧠 Introduction

The **AI Civic Intelligence System** is an **Agentic AI-based platform** designed to automate the detection, reporting, and verification of civic infrastructure issues such as potholes, garbage accumulation, and road damage.

The goal of this system is to reduce manual intervention, improve response time from authorities, and create a **smart, automated civic monitoring solution** using AI and intelligent workflows.

---

## 🎯 Problem Statement

In traditional systems:
- Civic issues are reported manually  
- No proper prioritization  
- Delays in response and resolution  
- Lack of verification after issue resolution  

👉 This project solves these problems using **AI + automation + multi-agent workflows**

---

## 🧠 Core Idea

The system uses:
- **Computer Vision (YOLO)** → to detect issues  
- **Agentic AI (LangGraph + MCP)** → to manage workflow decisions  
- **Automation (SendGrid)** → to notify departments  
- **Verification logic** → to confirm issue resolution  

---


---

## 🔍 Key Components Explained

### 1. 🧠 AI-Based Issue Detection
- Uses a **YOLO (You Only Look Once)** object detection model  
- Detects issues like:
  - Potholes  
  - Garbage  
  - Road damage  
- Outputs:
  - Bounding boxes  
  - Confidence score  
  - Detected class  

---

### 2. 🤖 Agentic AI Workflow (LangGraph + MCP)

This is the **core innovation of the project**.

Instead of a single pipeline, the system uses **multiple intelligent agents**:

- Detection Agent → identifies issue  
- Routing Agent → decides department  
- Priority Agent → assigns severity  
- Notification Agent → sends email  
- Verification Agent → checks resolution  

👉 These agents coordinate using:
- **LangGraph** → workflow orchestration  
- **MCP (Multi-agent Control Protocol)** → structured execution  

---

### 3. 📍 Location Extraction

The system extracts location using two methods:

1. **EXIF Metadata (GPS)**  
   - Reads latitude & longitude from image  

2. **OCR (Tesseract)**  
   - Extracts location text from image  

👉 Ensures location availability even without GPS  

---

### 4. 🚦 Severity & Priority Classification

The system assigns priority levels:
- Low  
- Medium  
- High  

Based on:
- Detection area  
- Confidence score  
- Issue type  

---

### 5. 📩 Automated Notification System

- Uses **SendGrid API**  
- Sends structured email containing:
  - Issue type  
  - Priority  
  - Location  
  - Image evidence  

---

### 6. 🔄 Verification Pipeline

Workflow:
- Authority uploads resolved image  
- System compares:
  - Original image  
  - Resolved image  

- AI verifies resolution  

👉 Ensures accountability and transparency  

---

### 7. 🖼️ Image Comparison System

- Displays:
  - Before image (issue)  
  - After image (resolved)  

---


---

## 🛠️ Tech Stack

### Backend
- FastAPI  

### Frontend
- Streamlit  

### AI/ML
- YOLO  

### Workflow
- LangGraph  
- MCP  

### Image Processing
- OpenCV  
- Pillow  

### OCR
- Tesseract  

### Notifications
- SendGrid  

---

## 💡 Key Innovations

- Agentic AI with multi-agent coordination  
- Modular workflow architecture  
- Integration of ML + automation + decision systems  
- Full issue lifecycle management  

---

## 🌍 Real-World Impact

- Enables smart city infrastructure monitoring  
- Reduces manual effort  
- Improves response time  
- Ensures verified resolution  
- Scalable for real-world deployment  

---

## 🚀 Future Enhancements

- Real-time dashboard  
- Map-based visualization  
- Mobile app integration  
- Cloud storage for images  
- Advanced AI verification  

---

## 🎯 Conclusion

This project demonstrates how **Agentic AI, computer vision, and automation** can be combined to build a **real-world intelligent system** that not only detects problems but also ensures they are resolved efficiently.

It goes beyond traditional ML systems by introducing **decision-making agents and end-to-end automation**, making it a **production-level smart city solution**.
