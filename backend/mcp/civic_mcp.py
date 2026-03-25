"""
Civic MCP Server
----------------
Registers Civic AI tools for agent use.
"""
import base64

#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

from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId
import json
from fastmcp import FastMCP
from backend.tool.yolo import run_detection
from backend.tool.gps import extract_gps
from backend.tool.notify import send_notification
from backend.tool.db_tool import insert_issue
from backend.config import DEPARTMENT_MAP, DEFAULT_DEPARTMENT, DEFAULT_EMAIL
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


mcp = FastMCP("civic")

# ===============================
# DETECTION
# ===============================
@mcp.tool()
def detect_issue(image_path: str):
    return run_detection(image_path)


# ===============================
# GPS
# ===============================
@mcp.tool()
def get_location(image_path: str):
    lat, lon,location_name = extract_gps(image_path)
    return {
    "lat": lat,
    "lon": lon,
    "location_name": location_name
}


# ===============================
# ROUTING
# ===============================
@mcp.tool()
def route_department(issue_type: str):
    dept = DEPARTMENT_MAP.get(issue_type)

    if dept:
        return dept

    return {
        "department": DEFAULT_DEPARTMENT,
        "email": DEFAULT_EMAIL
    }


# ===============================
# STORE ISSUE
# ===============================
@mcp.tool()
def store_issue(
    image_path: str,
    issue_type: str,
    confidence: float,
    annotated_image:str|None,
    bbox: list,
    area: float,
    detections: int,
    issue_detected: bool,
    lat: float | None,
    lon: float | None,
    severity: float,
    priority: str,
    department: str,
    email: str,
    status: str
):
    """
    Stores the issue in the database.
    Extra detection fields are accepted but not stored.
    """

    data = {
        "image_path": image_path,
        "issue_type": issue_type,
        "annotated_image": annotated_image,
        "lat": lat,
        "lon": lon,
        "severity": severity,
        "priority": priority,
        "department": department,
        "status": status
    }

    insert_issue(data)

    return {"stored": True}


# ===============================
# NOTIFY
# ===============================
@mcp.tool()
def notify(email: str, subject: str, message: str):
    ok = send_notification(email, subject, message)
    return {"sent": ok}


# ===============================
# VERIFY DETECTION
# ===============================
@mcp.tool()
def verify_issue(image_path: str):
    return run_detection(image_path)

from openai import OpenAI

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

from typing import Optional, List

from typing import Optional

@mcp.tool()
def generate_notification(
    issue_type: str,
    priority: str,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    department: str = "General Department"
):
    """
    Uses LLM to generate a civic notification message.
    """

    location = "Location unavailable" if lat is None or lon is None else f"({lat}, {lon})"

    prompt = f"""
You are a civic infrastructure monitoring assistant.

Generate an official notification for a municipal department.

Return the result in JSON format:

{{
  "subject": "...",
  "message": "..."
}}

Issue Details:
Issue Type: {issue_type}
Priority: {priority}
Location: {location}
Department: {department}

Write a short professional message requesting the department to inspect and resolve the issue.
"""

    resp = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = resp.choices[0].message.content

    try:
        result = json.loads(content)
        subject = result.get("subject", "Civic Issue Detected")
        message = result.get("message", content)
    except Exception:
        subject = "Civic Issue Detected"
        message = content

    return {
        "subject": subject,
        "message": message
    }

# ===============================
# NOTIFY + GENERATE MESSAGE
# ===============================
@mcp.tool()
def send_issue_notification(
    email: str,
    issue_type: str,
    department: str,
    priority: str,
    location_name: str,
    lat: float|None,
    lon: float|None,
    image_path: str
):
    """
    Sends civic issue notification email using SendGrid API.
    """
    import base64
    import os

    try:

        subject = f"Civic Issue Detected – {issue_type}"

        coords = (
            f"{lat}, {lon}"
            if lat is not None and lon is not None
            else "Not Available"
        )

        maps_link = (
            f"https://www.google.com/maps?q={lat},{lon}"
            if lat is not None and lon is not None
            else None
        )

        # ✅ FIX: use image_path + absolute path
        full_path = os.path.abspath(image_path)
        print("Reading:", full_path)

        encoded_image = None
        if os.path.exists(full_path):
            with open(full_path, "rb") as f:
                encoded_image = base64.b64encode(f.read()).decode()

        # detect mime type
        ext = image_path.split(".")[-1].lower()
        mime = "jpeg" if ext in ["jpg", "jpeg"] else "png"

        html_message = f"""
        <div style="font-family: Arial, sans-serif; padding: 10px;">

        <h2 style="color:#d32f2f;">🚨 Civic Issue Detected</h2>

        <p><b>Issue Type:</b> {issue_type}</p>
        <p><b>Priority:</b> {priority}</p>

        <p><b>Location:</b><br>
        {location_name}<br>
        <b>Coordinates:</b> {coords}</p>
        """

        if maps_link:
            html_message += f"""
        <p>
        <a href="{maps_link}" target="_blank">
        📍 View on Google Maps
        </a>
        </p>
        """

        # ✅ IMAGE BLOCK
            # ✅ IMAGE BLOCK (Updated to use cid)
        mail = Mail(
            from_email="eshwar77788@gmail.com",
            to_emails=email,
            subject=subject,
            html_content=html_message
        )
        # ✅ ATTACH THE IMAGE INLINE SO GMAIL CAN RENDER IT
        if encoded_image:
            attachment = Attachment()
            attachment.file_content = FileContent(encoded_image)
            attachment.file_type = FileType(f"image/{mime}")
            attachment.file_name = FileName(f"evidence.{ext}")
            attachment.disposition = Disposition("inline")
            attachment.content_id = ContentId("evidence_img")
            mail.attachment = attachment  # attaches the image to the email
        api_key = "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"
        sg = SendGridAPIClient(api_key)


        response = sg.send(mail)

        print("SendGrid status:", response.status_code)
        print("SendGrid body:", response.body)
        print("SendGrid headers:", response.headers)

        return {
            "sent": True,
            "status_code": response.status_code,
            "email": email,
            "subject": subject
        }

    except Exception as e:
        return {
            "sent": False,
            "error": str(e)
        }


@mcp.tool()
def send_resolution_notification(
        email: str,
        issue_type: str,
        department: str,
        location_name: str,
        lat: float,
        lon: float,
        original_image: str,
        resolved_image: str
):
    """
    Sends resolution confirmation email to department with inline image attachments.
    """
    import os
    import base64
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId

    try:
        subject = f"✅ Issue Resolved – {issue_type}"

        coords = f"{lat}, {lon}" if lat is not None and lon is not None else "Not Available"
        maps_link = f"https://www.google.com/maps?q={lat},{lon}" if lat is not None and lon is not None else None

        # Helper to read and encode images
        def read_image_base64(path):
            try:
                full_path = os.path.abspath(path)
                if os.path.exists(full_path):
                    with open(full_path, "rb") as f:
                        return base64.b64encode(f.read()).decode()
            except Exception as e:
                print(f"Error reading {path}:", e)
            return None

        original_encoded = read_image_base64(original_image)
        resolved_encoded = read_image_base64(resolved_image)

        # Helper to determine mime type
        def get_mime(path):
            ext = path.split(".")[-1].lower()
            return "jpeg" if ext in ["jpg", "jpeg"] else "png"

        # 1. Build the HTML Content using cid references
        html_message1 = f"""
        <div style="font-family: Arial, sans-serif; padding: 12px;">

        <h2 style="color:#2e7d32;">✅ Issue Successfully Resolved</h2>
        <p>Dear <b>{department}</b>,</p>
        <p>Thank you for addressing the reported civic issue. The resolution has been <b>verified by the Civic AI system</b>.</p>

        <hr/>
        <p><b>Issue Type:</b> {issue_type}</p>
        <p><b>Location:</b><br>{location_name}<br><b>Coordinates:</b> {coords}</p>
        """

        if maps_link:
            html_message1 += f'<p><a href="{maps_link}" target="_blank">📍 View Location on Google Maps</a></p>'

        html_message1 += "<hr/>"

        # Reference original image via CID
        if original_encoded:
            html_message1 += f"""
        <p><b>📷 Original Issue Image:</b></p>
        <img src="cid:original_img" width="350" style="border:1px solid #ccc; border-radius:8px; margin-bottom:10px;"/>
        """

        # Reference resolved image via CID
        if resolved_encoded:
            html_message1 += f"""
        <p><b>🛠️ Resolved Image:</b></p>
        <img src="cid:resolved_img" width="350" style="border:1px solid #ccc; border-radius:8px;"/>
        """

        html_message1 += """
        <hr/>
        <p>We appreciate your prompt action in maintaining civic infrastructure.</p>
        <p>Best regards,<br><b>Civic AI Monitoring System</b></p>
        </div>
        """

        # 2. Create the Mail object
        mail = Mail(
            from_email="eshwar77788@gmail.com",
            to_emails=email,
            subject=subject,
            html_content=html_message1
        )

        # 3. Helper function to attach files to the Mail object
        def attach_inline_image(mail_obj, b64_data, file_path, cid):
            if b64_data:
                mime_type = get_mime(file_path)
                file_name = os.path.basename(file_path)

                attachment = Attachment()
                attachment.file_content = FileContent(b64_data)
                attachment.file_type = FileType(f"image/{mime_type}")
                attachment.file_name = FileName(file_name)
                attachment.disposition = Disposition("inline")
                attachment.content_id = ContentId(cid)

                mail_obj.add_attachment(attachment)

        # Attach both images if they exist
        attach_inline_image(mail, original_encoded, original_image, "original_img")
        attach_inline_image(mail, resolved_encoded, resolved_image, "resolved_img")

        # 4. Send the Email
        # (Reminder: Replace this with your newly generated key!)
        api_key = "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"
        sg = SendGridAPIClient(api_key)

        response = sg.send(mail)

        print("SendGrid status:", response.status_code)

        return {
            "sent": True,
            "status_code": response.status_code,
            "email": email,
            "subject": subject
        }

    except Exception as e:
        print("SendGrid Error:", e)
        return {
            "sent": False,
            "error": str(e)
        }