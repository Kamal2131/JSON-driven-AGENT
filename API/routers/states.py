from fastapi import APIRouter, Query
from typing import List
from models.schemas import StateResponse
from utils.data import STATES

router = APIRouter(prefix="/api/v1/states", tags=["States"])

@router.get("", response_model=dict)
def get_states(active: bool = Query(True, description="Filter by active states")):
    """Retrieve list of states where health insurance enrollment is available"""
    filtered_states = [s for s in STATES if s["active"] == active] if active else STATES
    return {
        "success": True,
        "data": filtered_states,
        "message": "States fetched successfully"
    }
