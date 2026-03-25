from backend.tool.gps import extract_gps


#def location_agent(state: dict) -> dict:

#    if "image_path" not in state:
#        return state

#    lat, lon = extract_gps(state["image_path"])

#    state["lat"] = lat
#    state["lon"] = lon

#    return state
import json
from backend.mcp.civic_mcp import mcp


async def location_agent(state: dict) -> dict:
    if "image_path" not in state:
        return state

    res = await mcp.call_tool("get_location", {
        "image_path": state["image_path"]
    })

    result = json.loads(res.content[0].text)

    state["lat"] = result["lat"]
    state["lon"] = result["lon"]
    state["location_name"]=result["location_name"]

    return state