# Health Insurance Enrollment API

FastAPI backend for a dynamic form-filling system with interdependent REST APIs.
Supports both path-based and query-based endpoints for dynamic agent workflows.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --reload
```

3. Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

4. Test the APIs:
```bash
python test_dynamic_agent.py
```

## API Flow

### Path-Based Flow (Legacy)
1. **GET /api/v1/states** - Get available states
2. **GET /api/v1/states/{state_id}/policies** - Get policies for a state
3. **GET /api/v1/policies/{policy_id}/plans** - Get plans for a policy
4. **GET /api/v1/plans/{plan_id}/programs** - Get programs for a plan
5. **GET /api/v1/programs/{program_id}/risk-types** - Get risk types for a program
6. **GET /api/v1/risk-types/{risk_type_id}/risk-levels** - Get risk levels for a risk type
7. **POST /api/v1/enrollment/identifier/create** - Create enrollment identifier

### Query-Based Flow (Dynamic Agent Compatible)
1. **GET /api/v1/states** - Get available states
2. **GET /api/v1/policies?state={state}** - Get policies by state name/ID
3. **GET /api/v1/plans?state={state}&policy={policy}** - Get plans by state and policy
4. **POST /api/v1/identifier/create** - Create identifier with all selections

## Example Usage

### Query-Based Workflow (For Dynamic Agent)
```bash
# Step 1: Get states
curl http://localhost:8000/api/v1/states

# Step 2: Get policies by state name
curl "http://localhost:8000/api/v1/policies?state=Gujarat"

# Step 3: Get plans by state and policy
curl "http://localhost:8000/api/v1/plans?state=Gujarat&policy=Health%20Policy"

# Step 4: Create identifier
curl -X POST http://localhost:8000/api/v1/identifier/create \
  -H "Content-Type: application/json" \
  -d '{
    "configuration_name": "enrollment_config_1",
    "state": "Gujarat",
    "policy": "Health Policy",
    "plan": "Gold",
    "applicant_first_name": "John",
    "applicant_last_name": "Doe",
    "applicant_email": "john@example.com"
  }'
```

### Path-Based Workflow (Legacy)
```bash
# Step 1: Get states
curl http://localhost:8000/api/v1/states

# Step 2: Get policies for Gujarat (ST001)
curl http://localhost:8000/api/v1/states/ST001/policies

# Step 3: Get plans for Health Policy (POL001)
curl http://localhost:8000/api/v1/policies/POL001/plans

# Step 4: Create enrollment identifier
curl -X POST http://localhost:8000/api/v1/enrollment/identifier/create \
  -H "Content-Type: application/json" \
  -d '{
    "state_id": "ST001",
    "policy_id": "POL001",
    "plan_id": "PLN001",
    "program_id": "PRG001",
    "risk_type_id": "RT002",
    "risk_level_id": "RL002",
    "applicant_details": {
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1990-01-15",
      "email": "john.doe@example.com",
      "phone": "+919876543210"
    }
  }'
```

## Project Structure

```
.
├── main.py                          # FastAPI app entry point
├── requirements.txt                 # Python dependencies
├── test_dynamic_agent.py           # Test script for dynamic agent APIs
├── API_DOCUMENTATION.md            # Detailed API documentation
├── models/
│   ├── __init__.py
│   └── schemas.py                  # Pydantic models
├── routers/
│   ├── __init__.py
│   ├── states.py                   # States endpoint
│   ├── policies.py                 # Policies endpoints (path & query)
│   ├── plans.py                    # Plans & programs endpoints (path & query)
│   ├── risks.py                    # Risk types & levels endpoints
│   ├── identifier.py               # Enrollment identifier endpoint (v1)
│   └── identifier_v2.py            # Identifier endpoint (v2 - dynamic agent)
├── utils/
│   ├── __init__.py
│   └── data.py                     # In-memory data store
└── example_configs/
    ├── create_identifier_config.json   # Example JSON config
    └── full_workflow_config.json       # Full workflow config
```

## Dynamic Agent Configuration

See `example_configs/` directory for JSON configuration examples that can be used by the dynamic agent system.

### Key Features for Dynamic Agent:
- Query parameter support for flexible API calls
- Response fields follow `classPlanList[].FieldName` notation
- Accepts both IDs and names for all parameters
- Dependency validation across all steps
- Structured response format for easy parsing
