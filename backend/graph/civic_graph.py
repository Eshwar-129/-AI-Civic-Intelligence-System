"""
Civic Graph
-----------
LangGraph orchestration for the Civic AI agent pipeline.

Pipeline:
Detection → Location → Severity → Routing → Notification → Verification
"""

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

# Import all agents
from backend.agents.detection_agent import detection_agent
from backend.agents.location_agent import location_agent
from backend.agents.severity import severity_agent
from backend.agents.routing import routing_agent
from backend.agents.notification import notification_agent
from backend.agents.verification import verification_agent


# =========================================================
# STATE SCHEMA
# =========================================================

class CivicState(TypedDict, total=False):
    # Input paths
    image_path: str
    verify_image_path: Optional[str]

    # Detection
    issue_type: str
    confidence: float
    bbox: list
    area: float
    detections: int
    annotated_image: str
    issue_detected: bool

    # Location
    lat: float|None
    lon: float|None
    location_name:str|None

    # Severity
    severity: float
    priority: str

    # Routing
    department: str
    email: str

    # Status
    status: str

    # Verification
    verification: str
    resolved_image:str


# =========================================================
# BUILD GRAPH
# =========================================================

builder = StateGraph(CivicState)

# Add nodes
builder.add_node("detect", detection_agent)
builder.add_node("locate", location_agent)
builder.add_node("severity", severity_agent)
builder.add_node("route", routing_agent)
builder.add_node("notify", notification_agent)
builder.add_node("verify", verification_agent)

# Entry point
builder.set_entry_point("detect")

# Main pipeline
builder.add_edge("detect", "locate")
builder.add_edge("locate", "severity")
builder.add_edge("severity", "route")
builder.add_edge("route", "notify")

# =========================================================
# CONDITIONAL — VERIFICATION
# =========================================================

def verification_condition(state: CivicState):
    """
    If verification image provided → run verification.
    Else → end after notification.
    """
    if state.get("verify_image_path"):
        return "verify"
    return END


builder.add_conditional_edges(
    "notify",
    verification_condition,
    {
        "verify": "verify",
        END: END
    }
)

# Verification ends workflow
builder.add_edge("verify", END)

# Compile graph
graph = builder.compile()