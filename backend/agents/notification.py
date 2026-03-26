from tool.db_tool import insert_issue
from tool.notify import send_notification
from config import STATUS_ASSIGNED
from openai import OpenAI

# OpenRouter client
#client = OpenAI(
#    base_url="https://openrouter.ai/api/v1",
#    api_key="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"
#)


#def notification_agent(state: dict) -> dict:
#
#    if not state.get("issue_detected", False):
#        return state
#
#    state["status"] = STATUS_ASSIGNED
#
#    # Store issue in DB
#    insert_issue(state)
#
#    # LLM message generation via OpenRouter
#    prompt = f"""
#You are a civic infrastructure monitoring assistant.
#
#Generate a concise official notification message to a municipal department.
#
#Issue: {state["issue_type"]}
#Priority: {state["priority"]}
#Location: ({state["lat"]}, {state["lon"]})
#Department: {state["department"]}
#
#Write a short actionable message.
#"""
#
#    resp = client.chat.completions.create(
#        model="openai/gpt-4o-mini",
#        messages=[{"role": "user", "content": prompt}],
#        temperature=0.2,
#    )
#
#    message = resp.choices[0].message.content
#
#    subject = f"Civic Issue Detected: {state['issue_type']}"
#
#    send_notification(state["email"], subject, message)
#
#    return state
import json
from mcp.civic_mcp import mcp
from config import STATUS_ASSIGNED


async def notification_agent(state: dict) -> dict:
    if not state.get("issue_detected", False):
        return state

    state["status"] = STATUS_ASSIGNED
    print("s ",state)
    # Store in DB
    await mcp.call_tool("store_issue", {
        "image_path": state["image_path"],
        "annotated_image": state.get("annotated_image"),  # safe
        "issue_type": state["issue_type"],
        "confidence": state["confidence"],
        "bbox": state["bbox"],
        "area": state["area"],
        "detections": state["detections"],
        "issue_detected": state["issue_detected"],
        "lat": state["lat"],
        "lon": state["lon"],
        "severity": state["severity"],
        "priority": state["priority"],
        "department": state["department"],
        "email": state["email"],
        "status": state["status"]
    })

    # Generate notification
    llm = await mcp.call_tool("generate_notification", {
        "issue_type": state["issue_type"],
        "priority": state.get("priority", "Normal"),
        "lat": state["lat"],
        "lon": state["lon"],
        "department": state["department"]
    })

    print("LLM RAW OUTPUT:", llm.content[0].text)

    llm_data = json.loads(llm.content[0].text)

    subject = llm_data.get("subject", f"Civic Issue Detected: {state['issue_type']}")
    message = llm_data.get("message", llm.content[0].text)
    #BASE_URL = "https://handmade-pool-com-bidding.trycloudflare.com"

    #image_url = f"{state['image_path'].replace('\\', '/')}"

    #print(image_url)
    await mcp.call_tool("send_issue_notification", {
        "email": state["email"],
        "issue_type": state["issue_type"],
        "department": state["department"],
        "priority": state["priority"],
        "location_name": state.get("location_name", "Unknown Location"),
        "lat": state["lat"],
        "lon": state["lon"],
        "image_path": state["image_path"]
    })

    return state
