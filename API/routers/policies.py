from fastapi import APIRouter, Path, Query, HTTPException
from typing import Optional
from utils.data import POLICIES, STATES

router = APIRouter(prefix="/api/v1", tags=["Policies"])

@router.get("/policies", response_model=dict)
def get_policies_by_state(
    state: str = Query(..., description="State name or ID"),
    category: Optional[str] = Query(None, description="Filter by policy category")
):
    """Retrieve available health insurance policies for a specific state (query param)"""
    state_obj = next((s for s in STATES if s["state_id"] == state or s["state_name"] == state), None)
    if not state_obj:
        raise HTTPException(status_code=404, detail="State not found")
    
    filtered_policies = [p for p in POLICIES if p["state_id"] == state_obj["state_id"]]
    if category:
        filtered_policies = [p for p in filtered_policies if p["category"] == category]
    
    return {
        "success": True,
        "classPlanList": [{**p, "PolicyId": p["policy_id"]} for p in filtered_policies],
        "message": "Policies fetched successfully"
    }

@router.get("/states/{state_id}/policies", response_model=dict)
def get_policies(
    state_id: str = Path(..., description="State ID from /states API"),
    category: Optional[str] = Query(None, description="Filter by policy category")
):
    """Retrieve available health insurance policies for a specific state"""
    if not any(s["state_id"] == state_id for s in STATES):
        raise HTTPException(status_code=404, detail="State not found")
    
    filtered_policies = [p for p in POLICIES if p["state_id"] == state_id]
    if category:
        filtered_policies = [p for p in filtered_policies if p["category"] == category]
    
    return {
        "success": True,
        "state_id": state_id,
        "data": filtered_policies,
        "message": "Policies fetched successfully"
    }
