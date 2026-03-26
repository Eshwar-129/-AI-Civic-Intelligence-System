import json
from mcp.civic_mcp import mcp
from config import (
    GPS_TOLERANCE,
    STATUS_CLOSED,
    STATUS_IN_PROGRESS,
    STATUS_REJECTED
)


async def verification_agent(state: dict) -> dict:

    if "verify_image_path" not in state:
        return state

    # store resolved image path for UI
    state["resolved_image"] = state["verify_image_path"]

    # =================================
    # Extract GPS from repaired image
    # =================================

    tool_result = await mcp.call_tool(
        "get_location",
        {"image_path": state["verify_image_path"]}
    )

    gps = json.loads(tool_result.content[0].text)

    new_lat = gps.get("lat")
    new_lon = gps.get("lon")

    old_lat = state.get("lat")
    old_lon = state.get("lon")

    # =================================
    # GPS Validation
    # =================================

    if new_lat is None or old_lat is None:
        state["verification"] = "GPS_UNAVAILABLE"
        return state

    if abs(new_lat - old_lat) > GPS_TOLERANCE or abs(new_lon - old_lon) > GPS_TOLERANCE:
        state["status"] = STATUS_REJECTED
        state["verification"] = "LOCATION_MISMATCH"
        return state

    # =================================
    # Run detection on repaired image
    # =================================

    tool_result = await mcp.call_tool(
        "detect_issue",
        {"image_path": state["verify_image_path"]}
    )

    result = json.loads(tool_result.content[0].text)

    # store annotated resolved image
    state["resolved_annotated"] = result.get("annotated_image")

    # =================================
    # Issue resolved
    # =================================

    if result.get("detections", 0) == 0:

        state["status"] = STATUS_CLOSED
        state["verification"] = "RESOLVED"

        # send resolution email (FIXED: Added location_name)
        await mcp.call_tool(
            "send_resolution_notification",
            {
                "email": state.get("email"),
                "issue_type": state.get("issue_type"),
                "department": state.get("department"),
                "location_name": state.get("location_name", "Unknown Location"), # ⭐ Added this line
                "lat": state.get("lat"),
                "lon": state.get("lon"),
                "original_image": state.get("annotated_image"),
                "resolved_image": state.get("resolved_annotated")
            }
        )

    # =================================
    # Issue still exists
    # =================================

    else:

        state["status"] = STATUS_IN_PROGRESS
        state["verification"] = "NOT_RESOLVED"

    return state
