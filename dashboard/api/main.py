"""FastAPI application exposing basic agent status."""

from fastapi import FastAPI

from . import state

app = FastAPI(title="EcoNexyz Dashboard")


@app.get("/")
def index():
    """Return instructions for available endpoints."""
    return {"message": "See /status for agent status and /messages for bus messages"}


@app.get("/status")
def get_status():
    """Return running status of agents."""
    return {
        "agents": [
            {"name": agent.name, "running": agent.running} for agent in state.agents
        ]
    }


@app.get("/messages")
def get_messages(page: int = 1, page_size: int = 50):
    """Return recently published messages with pagination."""
    bus = state.message_bus
    if bus and hasattr(bus, "get_messages"):
        messages = list(reversed(bus.get_messages()))
        start = max(page - 1, 0) * page_size
        end = start + page_size
        return {
            "page": page,
            "page_size": page_size,
            "total": len(messages),
            "messages": messages[start:end],
        }
    return {"messages": []}
