-- =====================================================
-- CIVIC AI DATABASE SCHEMA
-- =====================================================
CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    issue_type TEXT,
    latitude REAL,
    longitude REAL,

    severity REAL,
    priority TEXT,

    department TEXT,
    status TEXT,

    image_path TEXT,
    verify_image_path TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Optional: departments reference table (future expansion)
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_type TEXT,
    department TEXT,
    email TEXT
);