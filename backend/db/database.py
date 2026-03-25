"""
Database Layer
--------------
Handles SQLite connection, schema initialization,
and basic CRUD operations for Civic AI system.
"""

import os
import sqlite3
from typing import List, Dict, Any

from backend.config import DB_PATH


# =========================================================
# CONNECTION
# =========================================================

def get_connection() -> sqlite3.Connection:
    """
    Returns SQLite connection with row factory.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# Global connection used by tools / FastAPI
conn = get_connection()


# =========================================================
# INIT DATABASE
# =========================================================

def init_db():
    """
    Creates tables from schema.sql if not exist.
    """
    schema_path = os.path.join(
        os.path.dirname(__file__),
        "schema.sql"
    )

    with open(schema_path, "r") as f:
        sql = f.read()

    conn.executescript(sql)
    conn.commit()


# =========================================================
# INSERT ISSUE
# =========================================================

def insert_issue(data: Dict[str, Any]) -> int:
    """
    Inserts detected civic issue into DB.
    Returns inserted issue id.
    """

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO issues (
            issue_type,
            latitude,
            longitude,
            severity,
            priority,
            department,
            status,
            image_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("issue_type"),
            data.get("lat"),
            data.get("lon"),
            data.get("severity"),
            data.get("priority"),
            data.get("department"),
            data.get("status"),
            data.get("image_path"),
        ),
    )

    conn.commit()
    return cursor.lastrowid


# =========================================================
# UPDATE ISSUE STATUS
# =========================================================

def update_issue_status(issue_id: int, status: str):
    """
    Updates lifecycle status of issue.
    """
    conn.execute(
        """
        UPDATE issues
        SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (status, issue_id),
    )
    conn.commit()


# =========================================================
# UPDATE VERIFICATION IMAGE
# =========================================================

def update_verification(issue_id: int, verify_path: str):
    """
    Stores verification image path.
    """
    conn.execute(
        """
        UPDATE issues
        SET verify_image_path = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (verify_path, issue_id),
    )
    conn.commit()


# =========================================================
# FETCH ALL ISSUES
# =========================================================

def get_all_issues() -> List[Dict[str, Any]]:
    """
    Returns all issues for dashboard.
    """
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM issues
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    return [dict(row) for row in rows]


# =========================================================
# FETCH SINGLE ISSUE
# =========================================================

def get_issue(issue_id: int) -> Dict[str, Any] | None:
    """
    Returns single issue record.
    """
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM issues
        WHERE id = ?
        """,
        (issue_id,),
    )

    row = cursor.fetchone()

    return dict(row) if row else None