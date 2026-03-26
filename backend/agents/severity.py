from config import (
    AREA_WEIGHT,
    CONFIDENCE_WEIGHT,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PRIORITY_LOW
)


async def severity_agent(state: dict) -> dict:
    if not state.get("issue_detected", False):
        state["severity"] = 0.0
        state["priority"] = PRIORITY_LOW
        return state

    conf = state.get("confidence", 0.0)
    area = state.get("area", 0.0)

    severity = (CONFIDENCE_WEIGHT * conf) + (AREA_WEIGHT * area / 100000)

    state["severity"] = severity

    if severity > 0.7:
        state["priority"] = PRIORITY_HIGH
    elif severity > 0.4:
        state["priority"] = PRIORITY_MEDIUM
    else:
        state["priority"] = PRIORITY_LOW

    return state
