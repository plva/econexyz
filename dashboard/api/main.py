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
def get_messages():
    """Return recently published messages."""
    bus = state.message_bus
    if bus and hasattr(bus, "get_messages"):
        return {"messages": bus.get_messages()}
    return {"messages": []}
