from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class StateResponse(BaseModel):
    state_id: str
    state_name: str
    state_code: str
    region: str
    active: bool

class PolicyResponse(BaseModel):
    policy_id: str
    state_id: str
    policy_name: str
    category: str
    base_premium: float
    coverage_amount: float

class PlanResponse(BaseModel):
    plan_id: str
    policy_id: str
    plan_name: str
    tier: str
    premium_multiplier: float
    waiting_period_days: int

class ProgramResponse(BaseModel):
    program_id: str
    plan_id: str
    program_name: str
    program_type: str
    additional_cost: float

class RiskTypeResponse(BaseModel):
    risk_type_id: str
    program_id: str
    risk_type_name: str
    risk_category: str
    premium_impact_percentage: float
    requires_medical_exam: bool

class RiskLevelResponse(BaseModel):
    risk_level_id: str
    risk_type_id: str
    risk_level_name: str
    tier: str
    premium_adjustment: float

class ApplicantDetails(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    date_of_birth: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    email: EmailStr
    phone: str = Field(..., pattern=r'^\+?[0-9]{10,15}$')

class EnrollmentRequest(BaseModel):
    state_id: str
    policy_id: str
    plan_id: str
    program_id: str
    risk_type_id: str
    risk_level_id: str
    applicant_details: ApplicantDetails

class PremiumCalculation(BaseModel):
    base_premium: float
    plan_adjustment: float
    program_cost: float
    risk_adjustment: float
    total_premium: float
    currency: str = "INR"

class EnrollmentSummary(BaseModel):
    state: str
    policy: str
    plan: str
    program: str
    risk_type: str
    risk_level: str

class EnrollmentData(BaseModel):
    enrollment_id: str
    identifier_code: str
    status: str
    created_at: str
    summary: EnrollmentSummary
    premium_calculation: PremiumCalculation

class EnrollmentResponse(BaseModel):
    success: bool
    data: EnrollmentData
    message: str
