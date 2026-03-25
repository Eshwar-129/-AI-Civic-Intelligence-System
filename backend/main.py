"""
Civic AI FastAPI Backend
------------------------
Exposes detection, verification, and dashboard APIs
for the agentic civic intelligence system.
"""
from backend.tool.db_tool import get_issue, update_issue_status # Add update_issue_status here!
import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from backend.graph.civic_graph import graph
from backend.config import TEMP_DIR
from backend.tool.db_tool import init_db, conn,get_issue

from fastapi.staticfiles import StaticFiles



# =========================================================
# APP INIT
# =========================================================

app = FastAPI(
    title="Civic AI Backend",
    description="Agentic AI system for civic issue detection and tracking",
    version="1.0"
)
app.mount("/runs", StaticFiles(directory="runs"), name="runs")
# Allow frontend access (Streamlit / browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables
init_db()

# Ensure temp directory exists
os.makedirs(TEMP_DIR, exist_ok=True)

# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# =========================================================
# HELPER — SAVE UPLOAD
# =========================================================

def save_upload(file: UploadFile) -> str:
    """
    Saves uploaded file to temp directory and returns path.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    path = os.path.join(TEMP_DIR, file.filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return path

# =========================================================
# API — DETECT ISSUE
# =========================================================

@app.post("/detect")
async def detect_issue(file: UploadFile = File(...)):
    """
    Detect civic issue from uploaded image.
    """
    try:
        image_path = UPLOAD_DIR / file.filename

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        state = {"image_path": str(image_path)}

        # ✅ IMPORTANT: await graph
        result = await graph.ainvoke(state)


        annotated = result.get("annotated_image")

        if annotated:
            annotated = annotated.replace("\\", "/")
            annotated = annotated.split("runs/")[-1]
            annotated = f"http://localhost:8000/runs/{annotated}"

        return {
            "issue_type": result.get("issue_type"),
            "priority": result.get("priority"),
            "department": result.get("department"),
            "status": result.get("status"),
            "lat": result.get("lat"),
            "lon": result.get("lon"),
            "confidence": result.get("confidence"),
            "annotated_image": annotated,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================
# API — VERIFY RESOLUTION
# =========================================================

from fastapi import File, UploadFile, Form, HTTPException
# Make sure to import your DB tool here!
# from backend.tool.db_tool import get_issue

from fastapi import File, UploadFile, Form, HTTPException
# 1. ADD THIS IMPORT AT THE TOP OF YOUR FILE
from backend.config import DEPARTMENT_MAP, DEFAULT_EMAIL


@app.post("/verify")
async def verify_issue(
        file: UploadFile = File(...),
        issue_id: str = Form(...)
):
    try:
        image_path = save_upload(file)
        old_issue = get_issue(issue_id)

        if not old_issue:
            raise HTTPException(status_code=404, detail="Original issue not found in database.")

        # ==========================================
        # 2. THE FIX: RE-CALCULATE THE EMAIL HERE
        # ==========================================
        issue_type = old_issue.get("issue_type")
        dept_info = DEPARTMENT_MAP.get(issue_type)

        # If the map has an email for this issue, use it. Otherwise, use default.
        if dept_info:
            target_email = dept_info.get("email", DEFAULT_EMAIL)
        else:
            target_email = DEFAULT_EMAIL

        # 3. Inject BOTH the new image and the old DB data into the state
        state = {
            "verify_image_path": image_path,
            "lat": old_issue.get("lat"),
            "lon": old_issue.get("lon"),
            "annotated_image": old_issue.get("annotated_image"),
            "email": target_email,  # <--- NOW IT HAS A REAL EMAIL!
            "department": old_issue.get("department"),
            "issue_type": issue_type,
            "location_name": old_issue.get("location_name", "Unknown Location")
        }

        # 4. Run the verification pipeline
        # 4. Run the verification pipeline
        result = await graph.ainvoke(state)

        # ==========================================
        # 5. THE FIX: SAVE THE NEW STATUS TO THE DB
        # ==========================================
        new_status = result.get("status")
        if new_status:
            # We must convert issue_id to an integer for the database!
            update_issue_status(int(issue_id), new_status)

        return {
            "status": new_status,
            "verification": result.get("verification"),
            "original_image": result.get("annotated_image"),
            "resolved_image": result.get("resolved_image")
        }

    except Exception as e:
        print("Verification API Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
# =========================================================
# API — GET ALL ISSUES (Dashboard)
# =========================================================

@app.get("/issues")
def get_issues():
    """
    Returns all stored civic issues from database.
    Used for dashboard and analytics.
    """
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM issues ORDER BY created_at DESC")
    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]
    issues = [dict(zip(columns, row)) for row in rows]

    return issues


# =========================================================
# API — HEALTH CHECK
# =========================================================

@app.get("/")
def health():
    return {"status": "Civic AI backend running"}