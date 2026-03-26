"""
Database Tool
-------------
Handles SQLite operations for Civic AI system.
"""

import sqlite3
from config import DB_PATH


conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issues(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_type TEXT,
        latitude REAL,
        longitude REAL,
        severity REAL,
        priority TEXT,
        department TEXT,
        status TEXT,
        image_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_type TEXT,
        area TEXT,
        department TEXT,
        email TEXT
    )
    """)

    conn.commit()


def insert_issue(data: dict):
    cursor.execute("""
        INSERT INTO issues(
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
    """, (
        data.get("issue_type"),
        data.get("lat"),
        data.get("lon"),
        data.get("severity", 0),
        data.get("priority", "LOW"),
        data.get("department", "General Department"),
        data.get("status", "REPORTED"),
        data.get("image_path")
    ))

    conn.commit()


def update_issue_status(issue_id: int, status: str):
    cursor.execute(
        "UPDATE issues SET status=? WHERE id=?",
        (status, issue_id)
    )
    conn.commit()


def get_department(issue_type: str, area: str):
    cursor.execute("""
        SELECT department, email
        FROM departments
        WHERE issue_type=? AND area=?
        LIMIT 1
    """, (issue_type, area))

    row = cursor.fetchone()

    if row:
        return {"department": row[0], "email": row[1]}

    return None


def get_issue(issue_id):
    import sqlite3
    from backend.config import DB_PATH

    print(f"\n=== DEBUG: Searching for Issue ID: '{issue_id}' ===")

    try:
        # Force the ID to be a number instead of a string
        numeric_id = int(issue_id)

        # Open a safe, local connection
        local_conn = sqlite3.connect(DB_PATH)
        local_conn.row_factory = sqlite3.Row
        local_cursor = local_conn.cursor()

        # X-RAY: Print every ID currently in the database to the terminal
        local_cursor.execute("SELECT id FROM issues")
        all_ids = [row["id"] for row in local_cursor.fetchall()]
        print(f"=== DEBUG: IDs currently in the database: {all_ids} ===")

        # Now try to fetch the specific issue
        local_cursor.execute("SELECT * FROM issues WHERE id = ?", (numeric_id,))
        row = local_cursor.fetchone()

        if row:
            print(f"=== DEBUG: Success! Found Issue {numeric_id}. ===")
            issue_data = dict(row)

            # Map the database names to the AI State names
            issue_data["lat"] = issue_data.get("latitude")
            issue_data["lon"] = issue_data.get("longitude")
            issue_data["annotated_image"] = issue_data.get("image_path")

            local_conn.close()
            return issue_data

        print(f"=== DEBUG: FAILED. Issue {numeric_id} is not in the list of IDs above. ===")
        local_conn.close()
        return None

    except ValueError:
        print(f"=== DEBUG: FAILED. The frontend sent '{issue_id}', which is not a valid number. ===")
        return None
    except Exception as e:
        print(f"=== DEBUG: Database Error: {e} ===")
        return None
