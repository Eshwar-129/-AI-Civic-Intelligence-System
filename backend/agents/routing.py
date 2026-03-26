from config import DEPARTMENT_MAP, DEFAULT_DEPARTMENT, DEFAULT_EMAIL


#def routing_agent(state: dict) -> dict:
#
#    if not state.get("issue_detected", False):
#        return state
#
#    dept = DEPARTMENT_MAP.get(state["issue_type"])
#
#    if dept:
#        state["department"] = dept["department"]
#        state["email"] = dept["email"]
#    else:
#        state["department"] = DEFAULT_DEPARTMENT
#        state["email"] = DEFAULT_EMAIL
#
#    return state

import json
from mcp.civic_mcp import mcp


async def routing_agent(state: dict) -> dict:
    if not state.get("issue_detected", False):
        return state

    res = await mcp.call_tool("route_department", {
        "issue_type": state["issue_type"]
    })

    result = json.loads(res.content[0].text)

    state["department"] = result["department"]
    state["email"] = result["email"]

    return state
