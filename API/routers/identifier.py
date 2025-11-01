from fastapi import APIRouter, HTTPException
from models.schemas import EnrollmentRequest, EnrollmentResponse
from utils.data import STATES, POLICIES, PLANS, PROGRAMS, RISK_TYPES, RISK_LEVELS
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1/enrollment", tags=["Enrollment"])

@router.post("/identifier/create", response_model=dict)
def create_enrollment_identifier(request: EnrollmentRequest):
    """Create a unique enrollment identifier by consolidating all selections from the enrollment flow"""
    
    # Validate all dependencies
    state = next((s for s in STATES if s["state_id"] == request.state_id), None)
    if not state:
        raise HTTPException(status_code=404, detail="Invalid state_id")
    
    policy = next((p for p in POLICIES if p["policy_id"] == request.policy_id and p["state_id"] == request.state_id), None)
    if not policy:
        raise HTTPException(status_code=404, detail="Invalid policy_id or policy not available in selected state")
    
    plan = next((p for p in PLANS if p["plan_id"] == request.plan_id and p["policy_id"] == request.policy_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Invalid plan_id or plan not available for selected policy")
    
    program = next((p for p in PROGRAMS if p["program_id"] == request.program_id and p["plan_id"] == request.plan_id), None)
    if not program:
        raise HTTPException(status_code=404, detail="Invalid program_id or program not available for selected plan")
    
    risk_type = next((r for r in RISK_TYPES if r["risk_type_id"] == request.risk_type_id and r["program_id"] == request.program_id), None)
    if not risk_type:
        raise HTTPException(status_code=404, detail="Invalid risk_type_id or risk type not available for selected program")
    
    risk_level = next((r for r in RISK_LEVELS if r["risk_level_id"] == request.risk_level_id and r["risk_type_id"] == request.risk_type_id), None)
    if not risk_level:
        raise HTTPException(status_code=404, detail="Invalid risk_level_id or risk level not available for selected risk type")
    
    # Calculate premium
    base_premium = policy["base_premium"]
    plan_adjustment = base_premium * (plan["premium_multiplier"] - 1)
    program_cost = program["additional_cost"]
    risk_adjustment = (base_premium * risk_type["premium_impact_percentage"] / 100) + risk_level["premium_adjustment"]
    total_premium = base_premium + plan_adjustment + program_cost + risk_adjustment
    
    # Generate enrollment ID and identifier code
    enrollment_id = f"ENR{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4().int)[:6]}"
    identifier_code = f"{state['state_code']}-{policy['policy_name'][:2].upper()}-{plan['plan_name'][:4].upper()}-{program['program_name'][:2].upper()}-{risk_type['risk_type_name'][:2].upper()}-{risk_level['risk_level_name'][:2].upper()}-{datetime.now().strftime('%Y%m%d')}"
    
    response_data = {
        "enrollment_id": enrollment_id,
        "identifier_code": identifier_code,
        "status": "pending_verification",
        "created_at": datetime.now().isoformat(),
        "summary": {
            "state": state["state_name"],
            "policy": policy["policy_name"],
            "plan": plan["plan_name"],
            "program": program["program_name"],
            "risk_type": risk_type["risk_type_name"],
            "risk_level": risk_level["risk_level_name"]
        },
        "premium_calculation": {
            "base_premium": base_premium,
            "plan_adjustment": plan_adjustment,
            "program_cost": program_cost,
            "risk_adjustment": risk_adjustment,
            "total_premium": round(total_premium, 2),
            "currency": "INR"
        }
    }
    
    return {
        "success": True,
        "data": response_data,
        "message": "Enrollment identifier created successfully"
    }
