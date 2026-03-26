"""
Global configuration for Civic AI backend
-----------------------------------------
Centralizes paths, thresholds, constants, and status values.
"""

import os

# =========================================================
# BASE DIRECTORIES
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BACKEND_DIR = os.path.join(BASE_DIR, "backend")
MODELS_DIR = os.path.join(BACKEND_DIR, "model")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# Ensure temp directory exists
os.makedirs(TEMP_DIR, exist_ok=True)

# =========================================================
# MODEL CONFIGURATION
# =========================================================

YOLO_MODEL_PATH = r"model/best.pt"

# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DB_PATH = os.path.join(BASE_DIR, "civic_ai.db")

# =========================================================
# DETECTION SETTINGS
# =========================================================

CONFIDENCE_THRESHOLD = 0.25

# =========================================================
# GPS SETTINGS
# =========================================================

GPS_TOLERANCE = 0.0005  # ~50–70 meters

# =========================================================
# SEVERITY WEIGHTS
# =========================================================

AREA_WEIGHT = 0.4
CONFIDENCE_WEIGHT = 0.6

# =========================================================
# PRIORITY LEVELS
# =========================================================

PRIORITY_HIGH = "HIGH"
PRIORITY_MEDIUM = "MEDIUM"
PRIORITY_LOW = "LOW"

# =========================================================
# ISSUE TYPES
# =========================================================

ISSUE_ROAD_DAMAGE = "road_damage"

# =========================================================
# DEPARTMENT DEFAULTS
# =========================================================
DEPARTMENT_MAP = {
    "Electrical_Poles": {
        "department": "Electrical Department",
        "email": "eshwarsaravana0@gmail.com"
    },
    "Road_Signs": {
        "department": "Traffic Department",
        "email": "project77799@gmail.com"
    },
    "Garbage": {
        "department": "Sanitation Department",
        "email": "eshwarsaravana0@gmail.com"
    },
    "Potholes and Roadcracks": {
        "department": "Roads Department",
        "email": "project77799@gmail.com"
    }
}
DEFAULT_DEPARTMENT = "General Department"
DEFAULT_EMAIL = "general@gov.in"

# =========================================================
# STATUS VALUES
# =========================================================

STATUS_OPEN = "OPEN"
STATUS_ASSIGNED = "ASSIGNED"
STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_CLOSED = "CLOSED"
STATUS_REJECTED = "REJECTED_LOCATION_MISMATCH"
