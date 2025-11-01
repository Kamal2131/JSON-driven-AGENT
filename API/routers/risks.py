from fastapi import APIRouter, Path, HTTPException
from utils.data import RISK_TYPES, RISK_LEVELS, PROGRAMS

router = APIRouter(prefix="/api/v1", tags=["Risk Assessment"])

@router.get("/programs/{program_identifier}/risk-types", response_model=dict)
def get_risk_types(program_identifier: str = Path(..., description="Program ID or Program Name")):
    """Retrieve risk assessment types for underwriting based on selected program"""
    program = next((p for p in PROGRAMS if p["program_id"] == program_identifier or p["program_name"] == program_identifier), None)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    filtered_risk_types = [r for r in RISK_TYPES if r["program_id"] == program["program_id"]]
    
    return {
        "success": True,
        "program_id": program["program_id"],
        "program_name": program["program_name"],
        "data": filtered_risk_types,
        "message": "Risk types fetched successfully"
    }

@router.get("/risk-types/{risk_type_identifier}/risk-levels", response_model=dict)
def get_risk_levels(risk_type_identifier: str = Path(..., description="Risk Type ID or Risk Type Name")):
    """Retrieve granular risk level tiers within a risk type for precise underwriting"""
    risk_type = next((r for r in RISK_TYPES if r["risk_type_id"] == risk_type_identifier or r["risk_type_name"] == risk_type_identifier), None)
    if not risk_type:
        raise HTTPException(status_code=404, detail="Risk type not found")
    
    filtered_risk_levels = [r for r in RISK_LEVELS if r["risk_type_id"] == risk_type["risk_type_id"]]
    
    return {
        "success": True,
        "risk_type_id": risk_type["risk_type_id"],
        "risk_type_name": risk_type["risk_type_name"],
        "data": filtered_risk_levels,
        "message": "Risk levels fetched successfully"
    }
