# In-memory data store for health insurance enrollment system

STATES = [
    {"state_id": "ST001", "state_name": "Gujarat", "state_code": "GJ", "region": "Western", "active": True, "enrollment_start_date": "2024-01-01", "enrollment_end_date": "2024-12-31"},
    {"state_id": "ST002", "state_name": "Maharashtra", "state_code": "MH", "region": "Western", "active": True, "enrollment_start_date": "2024-01-01", "enrollment_end_date": "2024-12-31"},
    {"state_id": "ST003", "state_name": "Karnataka", "state_code": "KA", "region": "Southern", "active": True, "enrollment_start_date": "2024-01-01", "enrollment_end_date": "2024-12-31"},
    {"state_id": "ST004", "state_name": "Tamil Nadu", "state_code": "TN", "region": "Southern", "active": True, "enrollment_start_date": "2024-01-01", "enrollment_end_date": "2024-12-31"},
    {"state_id": "ST005", "state_name": "Delhi", "state_code": "DL", "region": "Northern", "active": True, "enrollment_start_date": "2024-01-01", "enrollment_end_date": "2024-12-31"}
]

POLICIES = [
    {"policy_id": "POL001", "state_id": "ST001", "policy_name": "Health Policy", "category": "individual", "base_premium": 5000, "coverage_amount": 500000, "description": "Comprehensive individual health coverage"},
    {"policy_id": "POL002", "state_id": "ST001", "policy_name": "Family Cover", "category": "family", "base_premium": 12000, "coverage_amount": 1000000, "description": "Family floater health insurance"},
    {"policy_id": "POL003", "state_id": "ST001", "policy_name": "Senior Citizen Plan", "category": "individual", "base_premium": 8000, "coverage_amount": 600000, "description": "Specialized plan for seniors"},
    {"policy_id": "POL004", "state_id": "ST002", "policy_name": "Corporate Health", "category": "corporate", "base_premium": 8000, "coverage_amount": 750000, "description": "Group health insurance"},
    {"policy_id": "POL005", "state_id": "ST002", "policy_name": "Health Policy", "category": "individual", "base_premium": 5500, "coverage_amount": 500000, "description": "Individual health coverage"},
    {"policy_id": "POL006", "state_id": "ST003", "policy_name": "Family Cover", "category": "family", "base_premium": 11000, "coverage_amount": 1000000, "description": "Family health insurance"},
    {"policy_id": "POL007", "state_id": "ST003", "policy_name": "Health Policy", "category": "individual", "base_premium": 5200, "coverage_amount": 500000, "description": "Basic health coverage"},
    {"policy_id": "POL008", "state_id": "ST004", "policy_name": "Health Policy", "category": "individual", "base_premium": 5300, "coverage_amount": 500000, "description": "Individual health plan"},
    {"policy_id": "POL009", "state_id": "ST004", "policy_name": "Family Cover", "category": "family", "base_premium": 11500, "coverage_amount": 1000000, "description": "Family health plan"},
    {"policy_id": "POL010", "state_id": "ST005", "policy_name": "Health Policy", "category": "individual", "base_premium": 6000, "coverage_amount": 500000, "description": "Premium health coverage"},
    {"policy_id": "POL011", "state_id": "ST005", "policy_name": "Corporate Health", "category": "corporate", "base_premium": 9000, "coverage_amount": 800000, "description": "Corporate group insurance"}
]

PLANS = [
    {"plan_id": "PLN001", "policy_id": "POL001", "plan_name": "Gold", "tier": "premium", "premium_multiplier": 1.5, "waiting_period_days": 30},
    {"plan_id": "PLN002", "policy_id": "POL001", "plan_name": "Silver", "tier": "standard", "premium_multiplier": 1.2, "waiting_period_days": 45},
    {"plan_id": "PLN003", "policy_id": "POL001", "plan_name": "Platinum", "tier": "elite", "premium_multiplier": 2.0, "waiting_period_days": 0},
    {"plan_id": "PLN004", "policy_id": "POL001", "plan_name": "Bronze", "tier": "basic", "premium_multiplier": 1.0, "waiting_period_days": 60},
    {"plan_id": "PLN005", "policy_id": "POL002", "plan_name": "Gold", "tier": "premium", "premium_multiplier": 1.5, "waiting_period_days": 30},
    {"plan_id": "PLN006", "policy_id": "POL002", "plan_name": "Silver", "tier": "standard", "premium_multiplier": 1.2, "waiting_period_days": 45},
    {"plan_id": "PLN007", "policy_id": "POL003", "plan_name": "Gold", "tier": "premium", "premium_multiplier": 1.4, "waiting_period_days": 30},
    {"plan_id": "PLN008", "policy_id": "POL004", "plan_name": "Platinum", "tier": "elite", "premium_multiplier": 2.0, "waiting_period_days": 0},
    {"plan_id": "PLN009", "policy_id": "POL004", "plan_name": "Gold", "tier": "premium", "premium_multiplier": 1.5, "waiting_period_days": 30},
    {"plan_id": "PLN010", "policy_id": "POL005", "plan_name": "Silver", "tier": "standard", "premium_multiplier": 1.2, "waiting_period_days": 45},
    {"plan_id": "PLN011", "policy_id": "POL006", "plan_name": "Gold", "tier": "premium", "premium_multiplier": 1.5, "waiting_period_days": 30},
    {"plan_id": "PLN012", "policy_id": "POL006", "plan_name": "Platinum", "tier": "elite", "premium_multiplier": 2.0, "waiting_period_days": 0},
    {"plan_id": "PLN013", "policy_id": "POL007", "plan_name": "Silver", "tier": "standard", "premium_multiplier": 1.2, "waiting_period_days": 45},
    {"plan_id": "PLN014", "policy_id": "POL008", "plan_name": "Gold", "tier": "premium", "premium_multiplier": 1.5, "waiting_period_days": 30},
    {"plan_id": "PLN015", "policy_id": "POL009", "plan_name": "Platinum", "tier": "elite", "premium_multiplier": 2.0, "waiting_period_days": 0},
    {"plan_id": "PLN016", "policy_id": "POL010", "plan_name": "Gold", "tier": "premium", "premium_multiplier": 1.5, "waiting_period_days": 30},
    {"plan_id": "PLN017", "policy_id": "POL011", "plan_name": "Silver", "tier": "standard", "premium_multiplier": 1.2, "waiting_period_days": 45}
]

PROGRAMS = [
    {"program_id": "PRG001", "plan_id": "PLN001", "program_name": "Wellness Plus", "program_type": "wellness", "additional_cost": 1500, "description": "Annual health checkups"},
    {"program_id": "PRG002", "plan_id": "PLN001", "program_name": "Chronic Care Management", "program_type": "chronic_care", "additional_cost": 3000, "description": "Diabetes and hypertension care"},
    {"program_id": "PRG003", "plan_id": "PLN001", "program_name": "Preventive Care", "program_type": "preventive", "additional_cost": 2000, "description": "Vaccination and screening"},
    {"program_id": "PRG004", "plan_id": "PLN002", "program_name": "Maternity Care", "program_type": "maternity", "additional_cost": 5000, "description": "Pre and post natal care"},
    {"program_id": "PRG005", "plan_id": "PLN002", "program_name": "Wellness Plus", "program_type": "wellness", "additional_cost": 1500, "description": "Health checkups"},
    {"program_id": "PRG006", "plan_id": "PLN003", "program_name": "Wellness Plus", "program_type": "wellness", "additional_cost": 1500, "description": "Premium wellness"},
    {"program_id": "PRG007", "plan_id": "PLN003", "program_name": "Chronic Care Management", "program_type": "chronic_care", "additional_cost": 3000, "description": "Comprehensive chronic care"},
    {"program_id": "PRG008", "plan_id": "PLN004", "program_name": "Basic Wellness", "program_type": "wellness", "additional_cost": 1000, "description": "Basic health checkup"},
    {"program_id": "PRG009", "plan_id": "PLN005", "program_name": "Wellness Plus", "program_type": "wellness", "additional_cost": 1500, "description": "Family wellness"},
    {"program_id": "PRG010", "plan_id": "PLN005", "program_name": "Maternity Care", "program_type": "maternity", "additional_cost": 5000, "description": "Maternity coverage"},
    {"program_id": "PRG011", "plan_id": "PLN006", "program_name": "Wellness Plus", "program_type": "wellness", "additional_cost": 1500, "description": "Health checkups"},
    {"program_id": "PRG012", "plan_id": "PLN007", "program_name": "Wellness Plus", "program_type": "wellness", "additional_cost": 1400, "description": "Senior wellness"},
    {"program_id": "PRG013", "plan_id": "PLN008", "program_name": "Corporate Wellness", "program_type": "wellness", "additional_cost": 1200, "description": "Employee wellness"},
    {"program_id": "PRG014", "plan_id": "PLN009", "program_name": "Wellness Plus", "program_type": "wellness", "additional_cost": 1500, "description": "Health checkups"},
    {"program_id": "PRG015", "plan_id": "PLN010", "program_name": "Wellness Plus", "program_type": "wellness", "additional_cost": 1500, "description": "Health checkups"}
]

RISK_TYPES = [
    {"risk_type_id": "RT001", "program_id": "PRG001", "risk_type_name": "Low Risk", "risk_category": "standard", "premium_impact_percentage": 0, "requires_medical_exam": False, "description": "Healthy lifestyle, no pre-existing conditions"},
    {"risk_type_id": "RT002", "program_id": "PRG001", "risk_type_name": "Medium Risk", "risk_category": "moderate", "premium_impact_percentage": 15, "requires_medical_exam": True, "description": "Some health concerns"},
    {"risk_type_id": "RT003", "program_id": "PRG001", "risk_type_name": "High Risk", "risk_category": "elevated", "premium_impact_percentage": 35, "requires_medical_exam": True, "description": "Significant health risks"},
    {"risk_type_id": "RT004", "program_id": "PRG002", "risk_type_name": "Low Risk", "risk_category": "standard", "premium_impact_percentage": 0, "requires_medical_exam": False, "description": "Controlled conditions"},
    {"risk_type_id": "RT005", "program_id": "PRG002", "risk_type_name": "Medium Risk", "risk_category": "moderate", "premium_impact_percentage": 15, "requires_medical_exam": True, "description": "Multiple conditions"},
    {"risk_type_id": "RT006", "program_id": "PRG002", "risk_type_name": "High Risk", "risk_category": "elevated", "premium_impact_percentage": 35, "requires_medical_exam": True, "description": "Complex conditions"},
    {"risk_type_id": "RT007", "program_id": "PRG003", "risk_type_name": "Low Risk", "risk_category": "standard", "premium_impact_percentage": 0, "requires_medical_exam": False, "description": "Standard preventive care"},
    {"risk_type_id": "RT008", "program_id": "PRG004", "risk_type_name": "Low Risk", "risk_category": "standard", "premium_impact_percentage": 0, "requires_medical_exam": False, "description": "Normal pregnancy"},
    {"risk_type_id": "RT009", "program_id": "PRG004", "risk_type_name": "Medium Risk", "risk_category": "moderate", "premium_impact_percentage": 10, "requires_medical_exam": True, "description": "High-risk pregnancy"},
    {"risk_type_id": "RT010", "program_id": "PRG005", "risk_type_name": "Low Risk", "risk_category": "standard", "premium_impact_percentage": 0, "requires_medical_exam": False, "description": "Healthy individual"}
]

RISK_LEVELS = [
    {"risk_level_id": "RL001", "risk_type_id": "RT001", "risk_level_name": "Tier 1", "tier": "basic", "premium_adjustment": 0, "description": "Minimal risk"},
    {"risk_level_id": "RL002", "risk_type_id": "RT002", "risk_level_name": "Tier 1", "tier": "basic", "premium_adjustment": 10, "description": "Lower medium risk"},
    {"risk_level_id": "RL003", "risk_type_id": "RT002", "risk_level_name": "Tier 2", "tier": "intermediate", "premium_adjustment": 20, "description": "Mid medium risk"},
    {"risk_level_id": "RL004", "risk_type_id": "RT002", "risk_level_name": "Tier 3", "tier": "advanced", "premium_adjustment": 30, "description": "Upper medium risk"},
    {"risk_level_id": "RL005", "risk_type_id": "RT003", "risk_level_name": "Tier 1", "tier": "basic", "premium_adjustment": 25, "description": "Lower high risk"},
    {"risk_level_id": "RL006", "risk_type_id": "RT003", "risk_level_name": "Tier 2", "tier": "intermediate", "premium_adjustment": 35, "description": "Mid high risk"},
    {"risk_level_id": "RL007", "risk_type_id": "RT003", "risk_level_name": "Tier 3", "tier": "advanced", "premium_adjustment": 50, "description": "Upper high risk"},
    {"risk_level_id": "RL008", "risk_type_id": "RT004", "risk_level_name": "Tier 1", "tier": "basic", "premium_adjustment": 0, "description": "Controlled chronic"},
    {"risk_level_id": "RL009", "risk_type_id": "RT005", "risk_level_name": "Tier 1", "tier": "basic", "premium_adjustment": 15, "description": "Multiple chronic"},
    {"risk_level_id": "RL010", "risk_type_id": "RT005", "risk_level_name": "Tier 2", "tier": "intermediate", "premium_adjustment": 25, "description": "Complex chronic"},
    {"risk_level_id": "RL011", "risk_type_id": "RT006", "risk_level_name": "Tier 1", "tier": "basic", "premium_adjustment": 30, "description": "Severe chronic"},
    {"risk_level_id": "RL012", "risk_type_id": "RT007", "risk_level_name": "Tier 1", "tier": "basic", "premium_adjustment": 0, "description": "Standard preventive"},
    {"risk_level_id": "RL013", "risk_type_id": "RT008", "risk_level_name": "Tier 1", "tier": "basic", "premium_adjustment": 0, "description": "Normal maternity"},
    {"risk_level_id": "RL014", "risk_type_id": "RT009", "risk_level_name": "Tier 1", "tier": "basic", "premium_adjustment": 10, "description": "High-risk maternity"},
    {"risk_level_id": "RL015", "risk_type_id": "RT010", "risk_level_name": "Tier 1", "tier": "basic", "premium_adjustment": 0, "description": "Healthy wellness"}
]
