from fastapi import APIRouter, Path, Query, HTTPException
from typing import Optional
from utils.data import PLANS, POLICIES, PROGRAMS, STATES

router = APIRouter(prefix="/api/v1", tags=["Plans"])

@router.get("/plans", response_model=dict)
def get_plans_by_query(
    state: str = Query(..., description="State name or ID"),
    policy: str = Query(..., description="Policy name or ID"),
    min_coverage: Optional[float] = Query(None, description="Minimum coverage amount filter")
):
    """Retrieve available insurance plans for a specific state and policy (query params)"""
    state_obj = next((s for s in STATES if s["state_id"] == state or s["state_name"] == state), None)
    if not state_obj:
        raise HTTPException(status_code=404, detail="State not found")
    
    policy_obj = next((p for p in POLICIES if (p["policy_id"] == policy or p["policy_name"] == policy) and p["state_id"] == state_obj["state_id"]), None)
    if not policy_obj:
        raise HTTPException(status_code=404, detail="Policy not found for the given state")
    
    filtered_plans = [p for p in PLANS if p["policy_id"] == policy_obj["policy_id"]]
    
    return {
        "success": True,
        "classPlanList": [{**p, "PlanDescription": p["plan_name"]} for p in filtered_plans],
        "message": "Plans fetched successfully"
    }

@router.get("/policies/{policy_id}/plans", response_model=dict)
def get_plans(
    policy_id: str = Path(..., description="Policy ID from /policies API"),
    min_coverage: Optional[float] = Query(None, description="Minimum coverage amount filter")
):
    """Retrieve available insurance plans for a specific policy"""
    if not any(p["policy_id"] == policy_id for p in POLICIES):
        raise HTTPException(status_code=404, detail="Policy not found")
    
    filtered_plans = [p for p in PLANS if p["policy_id"] == policy_id]
    
    return {
        "success": True,
        "policy_id": policy_id,
        "data": filtered_plans,
        "message": "Plans fetched successfully"
    }

@router.get("/plans/{plan_identifier}/programs", response_model=dict)
def get_programs(
    plan_identifier: str = Path(..., description="Plan ID or Plan Name"),
    program_type: Optional[str] = Query(None, description="Filter by program type")
):
    """Retrieve available health programs under a specific plan"""
    plan = next((p for p in PLANS if p["plan_id"] == plan_identifier or p["plan_name"] == plan_identifier), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    filtered_programs = [p for p in PROGRAMS if p["plan_id"] == plan["plan_id"]]
    if program_type:
        filtered_programs = [p for p in filtered_programs if p["program_type"] == program_type]
    
    return {
        "success": True,
        "plan_id": plan["plan_id"],
        "plan_name": plan["plan_name"],
        "data": filtered_programs,
        "message": "Programs fetched successfully"
    }
