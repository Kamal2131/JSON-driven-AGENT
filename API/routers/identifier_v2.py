from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils.data import STATES, POLICIES, PLANS, PROGRAMS, RISK_TYPES, RISK_LEVELS
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1", tags=["Identifier V2"])

class IdentifierRequest(BaseModel):
    configuration_name: Optional[str] = None
    state: str
    policy: str
    plan: str
    program: Optional[str] = None
    risk_type: Optional[str] = None
    risk_level: Optional[str] = None
    applicant_first_name: Optional[str] = None
    applicant_last_name: Optional[str] = None
    applicant_email: Optional[str] = None

@router.post("/identifier/create", response_model=dict)
def create_identifier_flexible(request: IdentifierRequest):
    """Create enrollment identifier accepting names or IDs"""
    
    # Find state
    state = next((s for s in STATES if s["state_id"] == request.state or s["state_name"] == request.state), None)
    if not state:
        raise HTTPException(status_code=404, detail="State not found")
    
    # Find policy
    policy = next((p for p in POLICIES if (p["policy_id"] == request.policy or p["policy_name"] == request.policy) and p["state_id"] == state["state_id"]), None)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found for state")
    
    # Find plan
    plan = next((p for p in PLANS if (p["plan_id"] == request.plan or p["plan_name"] == request.plan) and p["policy_id"] == policy["policy_id"]), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found for policy")
    
    # Optional: Find program
    program = None
    program_cost = 0
    if request.program:
        program = next((p for p in PROGRAMS if (p["program_id"] == request.program or p["program_name"] == request.program) and p["plan_id"] == plan["plan_id"]), None)
        if program:
            program_cost = program["additional_cost"]
    
    # Optional: Find risk type
    risk_type = None
    risk_adjustment = 0
    if request.risk_type and program:
        risk_type = next((r for r in RISK_TYPES if (r["risk_type_id"] == request.risk_type or r["risk_type_name"] == request.risk_type) and r["program_id"] == program["program_id"]), None)
        if risk_type:
            risk_adjustment = policy["base_premium"] * risk_type["premium_impact_percentage"] / 100
    
    # Optional: Find risk level
    risk_level = None
    if request.risk_level and risk_type:
        risk_level = next((r for r in RISK_LEVELS if (r["risk_level_id"] == request.risk_level or r["risk_level_name"] == request.risk_level) and r["risk_type_id"] == risk_type["risk_type_id"]), None)
        if risk_level:
            risk_adjustment += risk_level["premium_adjustment"]
    
    # Calculate premium
    base_premium = policy["base_premium"]
    plan_adjustment = base_premium * (plan["premium_multiplier"] - 1)
    total_premium = base_premium + plan_adjustment + program_cost + risk_adjustment
    
    # Generate IDs
    enrollment_id = f"ENR{datetime.now().strftime('%Y%m%d%H%M%S')}"
    identifier_code = f"{state['state_code']}-{policy['policy_name'][:3].upper()}-{plan['plan_name'][:3].upper()}-{datetime.now().strftime('%Y%m%d')}"
    
    response_data = {
        "enrollment_id": enrollment_id,
        "identifier_code": identifier_code,
        "configuration_name": request.configuration_name,
        "status": "created",
        "created_at": datetime.now().isoformat(),
        "state": state["state_name"],
        "policy": policy["policy_name"],
        "plan": plan["plan_name"],
        "program": program["program_name"] if program else None,
        "risk_type": risk_type["risk_type_name"] if risk_type else None,
        "risk_level": risk_level["risk_level_name"] if risk_level else None,
        "applicant": {
            "first_name": request.applicant_first_name,
            "last_name": request.applicant_last_name,
            "email": request.applicant_email
        } if request.applicant_first_name else None,
        "premium": {
            "base_premium": base_premium,
            "plan_adjustment": round(plan_adjustment, 2),
            "program_cost": program_cost,
            "risk_adjustment": round(risk_adjustment, 2),
            "total_premium": round(total_premium, 2),
            "currency": "INR"
        }
    }
    
    return {
        "success": True,
        "data": response_data,
        "message": "Identifier created successfully"
    }
