# API Documentation for Dynamic Agent System

## Overview
This API system supports both path-based and query-based endpoints to enable dynamic agent workflows.

## Base URL
```
http://localhost:8000/api/v1
```

## Endpoints

### 1. Get States
**Path-based:**
```
GET /api/v1/states
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "state_id": "ST001",
      "state_name": "Gujarat",
      "state_code": "GJ",
      "region": "Western",
      "active": true
    }
  ],
  "message": "States fetched successfully"
}
```

---

### 2. Get Policies

**Query-based (for dynamic agent):**
```
GET /api/v1/policies?state={state}
```

**Parameters:**
- `state` (query, required): State name or ID

**Response:**
```json
{
  "success": true,
  "classPlanList": [
    {
      "policy_id": "POL001",
      "PolicyId": "POL001",
      "state_id": "ST001",
      "policy_name": "Health Policy",
      "category": "individual",
      "base_premium": 5000,
      "coverage_amount": 500000
    }
  ],
  "message": "Policies fetched successfully"
}
```

**Path-based (legacy):**
```
GET /api/v1/states/{state_id}/policies
```

---

### 3. Get Plans

**Query-based (for dynamic agent):**
```
GET /api/v1/plans?state={state}&policy={policy}
```

**Parameters:**
- `state` (query, required): State name or ID
- `policy` (query, required): Policy name or ID

**Response:**
```json
{
  "success": true,
  "classPlanList": [
    {
      "plan_id": "PLN001",
      "policy_id": "POL001",
      "plan_name": "Gold",
      "PlanDescription": "Gold",
      "tier": "premium",
      "premium_multiplier": 1.5,
      "waiting_period_days": 30
    }
  ],
  "message": "Plans fetched successfully"
}
```

**Path-based (legacy):**
```
GET /api/v1/policies/{policy_id}/plans
```

---

### 4. Get Programs
```
GET /api/v1/plans/{plan_id}/programs
```

**Response:**
```json
{
  "success": true,
  "plan_id": "PLN001",
  "data": [
    {
      "program_id": "PRG001",
      "plan_id": "PLN001",
      "program_name": "Wellness Plus",
      "program_type": "wellness",
      "additional_cost": 1500
    }
  ],
  "message": "Programs fetched successfully"
}
```

---

### 5. Get Risk Types
```
GET /api/v1/programs/{program_id}/risk-types
```

**Response:**
```json
{
  "success": true,
  "program_id": "PRG001",
  "data": [
    {
      "risk_type_id": "RT001",
      "program_id": "PRG001",
      "risk_type_name": "Low Risk",
      "risk_category": "standard",
      "premium_impact_percentage": 0,
      "requires_medical_exam": false
    }
  ],
  "message": "Risk types fetched successfully"
}
```

---

### 6. Get Risk Levels
```
GET /api/v1/risk-types/{risk_type_id}/risk-levels
```

**Response:**
```json
{
  "success": true,
  "risk_type_id": "RT002",
  "data": [
    {
      "risk_level_id": "RL001",
      "risk_type_id": "RT002",
      "risk_level_name": "Tier 1",
      "tier": "basic",
      "premium_adjustment": 10
    }
  ],
  "message": "Risk levels fetched successfully"
}
```

---

### 7. Create Identifier (V2 - Dynamic Agent Compatible)
```
POST /api/v1/identifier/create
```

**Request Body:**
```json
{
  "configuration_name": "enrollment_config_1",
  "state": "Gujarat",
  "policy": "Health Policy",
  "plan": "Gold",
  "program": "Wellness Plus",
  "risk_type": "Medium Risk",
  "risk_level": "Tier 2",
  "applicant_first_name": "John",
  "applicant_last_name": "Doe",
  "applicant_email": "john@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "configuration_name": "enrollment_config_1",
    "enrollment_id": "ENR20240115123456",
    "identifier_code": "GJ-HEA-GOL-20240115",
    "status": "created",
    "created_at": "2024-01-15T10:30:00",
    "summary": {
      "state": "Gujarat",
      "policy": "Health Policy",
      "plan": "Gold",
      "program": "Wellness Plus",
      "risk_type": "Medium Risk",
      "risk_level": "Tier 2"
    },
    "premium_calculation": {
      "base_premium": 5000,
      "plan_adjustment": 2500,
      "program_cost": 1500,
      "risk_adjustment": 770,
      "total_premium": 9770,
      "currency": "INR"
    },
    "applicant": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com"
    }
  },
  "message": "Identifier created successfully"
}
```

---

## Dynamic Agent JSON Configuration

### Example Configuration Structure
```json
{
  "api_name": "Create Identifier",
  "endpoint": "/identifier/create",
  "method": "POST",
  "description": "API configuration for creating an identifier",
  "parameters": {
    "configuration_name": {
      "type": "string",
      "required": true
    },
    "state": {
      "type": "string",
      "required": true
    },
    "policy": {
      "type": "string",
      "required": true,
      "depends_on": "state",
      "api_call": "/policies?state={state}",
      "response_field": "classPlanList[].PolicyId"
    },
    "plan": {
      "type": "string",
      "required": true,
      "depends_on": ["state", "policy"],
      "api_call": "/plans?state={state}&policy={policy}",
      "response_field": "classPlanList[].PlanDescription"
    }
  }
}
```

### Response Field Path Notation
- `data[]` - Array of objects in data field
- `data[].field_name` - Access field_name in each array element
- `classPlanList[].PolicyId` - Access PolicyId in classPlanList array
- `data.enrollment_id` - Direct field access

---

## Testing Examples

### Test Query-based Workflow
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
    "configuration_name": "test_config",
    "state": "Gujarat",
    "policy": "Health Policy",
    "plan": "Gold"
  }'
```

---

## Notes for Dynamic Agent Implementation

1. **Flexible Parameter Matching**: APIs accept both IDs and names for flexibility
2. **Response Structure**: Query-based endpoints use `classPlanList` for compatibility
3. **Dependency Chain**: Each step validates dependencies from previous steps
4. **Error Handling**: Returns 404 with descriptive messages for invalid dependencies
5. **Optional Parameters**: Program, risk_type, and risk_level are optional in identifier creation
