import json
from backend.mcp.civic_mcp import mcp

async def detection_agent(state: dict) -> dict:
    if "image_path" not in state:
        state["issue_detected"] = False
        return state

    tool_result = await mcp.call_tool(
        "detect_issue",
        {"image_path": state["image_path"]}
    )

    result_text = tool_result.content[0].text
    result = json.loads(result_text)
    state["issue_type"] = result["issue"]
    state["confidence"] = result["confidence"]
    state["bbox"] = result["bbox"]
    state["area"] = result["area"]
    state["detections"] = result["detections"]
    state["annotated_image"] = result["annotated_image"]   # ⭐ ADD THIS
    state["issue_detected"] = result["detections"] > 0


    return state