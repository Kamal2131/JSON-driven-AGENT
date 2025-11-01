# API Testing Guide

> ⚠️ **FOR TESTING PURPOSES ONLY**  
> This API is designed for testing the Dynamic AI Agent System. Not for production use.

---

## 🚀 Quick Start

### 1. Start the API Server
```bash
cd API
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Root Info**: http://localhost:8000/

---

## 📋 Available Endpoints

### **Health Insurance Endpoints**

#### 1. Get States
```http
GET /api/v1/states?active=true
```

**Response:**
```json
{
  "data": [
    {
      "state_id": "ST001",
      "state_name": "Gujarat",
      "state_code": "GJ",
      "region": "Western",
      "active": true
    }
  ]
}
```

---

#### 2. Get Policies
```http
GET /api/v1/policies?state=Gujarat
```

**Query Parameters:**
- `state` (required): State name or ID
- `category` (optional): Policy category

**Response:**
```json
{
  "classPlanList": [
    {
      "policy_id": "POL001",
      "policy_name": "Health Policy",
      "category": "individual",
      "base_premium": 5000,
      "coverage_amount": 500000
    }
  ]
}
```

---

#### 3. Get Plans
```http
GET /api/v1/plans?state=Gujarat&policy=Health Policy
```

**Query Parameters:**
- `state` (required): State name or ID
- `policy` (required): Policy name or ID
- `min_coverage` (optional): Minimum coverage amount

**Response:**
```json
{
  "classPlanList": [
    {
      "plan_id": "PLN001",
      "plan_name": "Gold",
      "tier": "premium",
      "premium_multiplier": 1.5,
      "waiting_period_days": 30
    }
  ]
}
```

---

#### 4. Get Programs
```http
GET /api/v1/plans/Gold/programs
```

**Path Parameters:**
- `plan_name_or_id`: Plan name or ID

**Response:**
```json
{
  "data": [
    {
      "program_id": "PRG001",
      "program_name": "Wellness Plus",
      "program_type": "wellness",
      "additional_cost": 1500
    }
  ]
}
```

---

#### 5. Get Risk Types
```http
GET /api/v1/programs/Wellness Plus/risk-types
```

**Path Parameters:**
- `program_name_or_id`: Program name or ID

**Response:**
```json
{
  "data": [
    {
      "risk_type_id": "RT001",
      "risk_type_name": "Low Risk",
      "risk_category": "standard",
      "premium_impact_percentage": 0
    }
  ]
}
```

---

#### 6. Get Risk Levels
```http
GET /api/v1/risk-types/Low Risk/risk-levels
```

**Path Parameters:**
- `risk_type_name_or_id`: Risk type name or ID

**Response:**
```json
{
  "data": [
    {
      "risk_level_id": "RL001",
      "risk_level_name": "Tier 1",
      "premium_adjustment": 0
    }
  ]
}
```

---

#### 7. Create Identifier
```http
POST /api/v1/identifier/create
Content-Type: application/json
```

**Request Body:**
```json
{
  "configuration_name": "Health_Identifier_Config",
  "state": "Gujarat",
  "policy": "Health Policy",
  "plan": "Gold",
  "program": "Wellness Plus",
  "risk_type": "Low Risk",
  "risk_level": "Tier 1",
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
    "enrollment_id": "ENR20251031194935",
    "identifier_code": "GJ-HEA-GOL-20251031",
    "status": "created",
    "state": "Gujarat",
    "policy": "Health Policy",
    "plan": "Gold",
    "program": "Wellness Plus",
    "risk_type": "Low Risk",
    "risk_level": "Tier 1",
    "applicant": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com"
    },
    "premium": {
      "base_premium": 5000,
      "plan_adjustment": 2500,
      "program_cost": 1500,
      "risk_adjustment": 0,
      "total_premium": 9000,
      "currency": "INR"
    },
    "created_at": "2025-10-31T19:49:35"
  },
  "message": "Identifier created successfully"
}
```

---

### **Dummy Test Endpoints**

#### 8. Get Countries
```http
GET /api/v1/dummy/countries
```

**Response:**
```json
{
  "data": [
    {"id": "IN", "name": "India"},
    {"id": "US", "name": "United States"},
    {"id": "UK", "name": "United Kingdom"}
  ]
}
```

---

#### 9. Get Cities
```http
GET /api/v1/dummy/cities?country=India
```

**Query Parameters:**
- `country` (required): Country name

**Response:**
```json
{
  "data": [
    {"id": "MUM", "name": "Mumbai"},
    {"id": "DEL", "name": "Delhi"},
    {"id": "BLR", "name": "Bangalore"}
  ]
}
```

---

#### 10. Get Categories
```http
GET /api/v1/dummy/categories
```

**Response:**
```json
{
  "data": [
    {"id": "electronics", "name": "Electronics"},
    {"id": "clothing", "name": "Clothing"},
    {"id": "books", "name": "Books"}
  ]
}
```

---

#### 11. Get Products
```http
GET /api/v1/dummy/products?category=electronics
```

**Query Parameters:**
- `category` (required): Category ID

**Response:**
```json
{
  "data": [
    {"id": "P001", "name": "Laptop", "price": 50000},
    {"id": "P002", "name": "Smartphone", "price": 30000}
  ]
}
```

---

#### 12. Create Order
```http
POST /api/v1/dummy/orders/create
Content-Type: application/json
```

**Request Body:**
```json
{
  "country": "India",
  "city": "Mumbai",
  "category": "electronics",
  "product": "P001",
  "quantity": 1,
  "customer_name": "John Doe",
  "customer_email": "john@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "order_id": "ORD20251031194935",
    "country": "India",
    "city": "Mumbai",
    "product": "Laptop",
    "quantity": 1,
    "customer": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "created_at": "2025-10-31T19:49:35"
  }
}
```

---

#### 13. Create Registration
```http
POST /api/v1/dummy/registrations/create
Content-Type: application/json
```

**Request Body:**
```json
{
  "country": "India",
  "city": "Mumbai",
  "user_name": "John Doe",
  "user_email": "john@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "registration_id": "REG20251031194935",
    "country": "India",
    "city": "Mumbai",
    "user": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "created_at": "2025-10-31T19:49:35"
  }
}
```

---

## 🧪 Testing with cURL

### Get States
```bash
curl http://localhost:8000/api/v1/states?active=true
```

### Get Policies
```bash
curl "http://localhost:8000/api/v1/policies?state=Gujarat"
```

### Create Identifier
```bash
curl -X POST http://localhost:8000/api/v1/identifier/create \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Gujarat",
    "policy": "Health Policy",
    "plan": "Gold",
    "applicant_first_name": "John",
    "applicant_last_name": "Doe",
    "applicant_email": "john@example.com"
  }'
```

### Create Order
```bash
curl -X POST http://localhost:8000/api/v1/dummy/orders/create \
  -H "Content-Type: application/json" \
  -d '{
    "country": "India",
    "city": "Mumbai",
    "category": "electronics",
    "product": "P001",
    "customer_name": "John Doe",
    "customer_email": "john@example.com"
  }'
```

---

## 🧪 Testing with PowerShell

### Get States
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/states?active=true"
```

### Create Identifier
```powershell
$body = @{
    state = "Gujarat"
    policy = "Health Policy"
    plan = "Gold"
    applicant_first_name = "John"
    applicant_last_name = "Doe"
    applicant_email = "john@example.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/identifier/create" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

---

## 📊 Test Data

### States (5)
- Gujarat (ST001)
- Maharashtra (ST002)
- Karnataka (ST003)
- Tamil Nadu (ST004)
- Delhi (ST005)

### Policies (11)
- Health Policy
- Family Cover
- Senior Citizen Plan
- Corporate Health

### Plans (17)
- Gold (Premium)
- Silver (Standard)
- Platinum (Elite)
- Bronze (Basic)

### Programs (15)
- Wellness Plus
- Chronic Care Management
- Maternity Care
- Preventive Care

### Risk Types (10)
- Low Risk
- Medium Risk
- High Risk

### Risk Levels (15)
- Tier 1
- Tier 2
- Tier 3

---

## 🔗 Dependencies

All endpoints support both **names** and **IDs**:

```
State → Policy → Plan → Program → Risk Type → Risk Level
```

**Example:**
- Get policies for "Gujarat" or "ST001"
- Get plans for "Health Policy" or "POL001"
- Get programs for "Gold" or "PLN001"

---

## ⚠️ Important Notes

1. **Testing Only**: This API uses in-memory data. Data resets on restart.
2. **No Authentication**: No auth required for testing.
3. **CORS Enabled**: All origins allowed for testing.
4. **Case Sensitive**: Names are case-sensitive ("Gujarat" ≠ "gujarat")
5. **Flexible Input**: Accepts both names and IDs for all parameters.

---

## 🐛 Common Issues

### Issue: 404 Not Found
**Solution**: Check if the state/policy/plan exists and spelling is correct.

### Issue: Empty Response
**Solution**: Ensure dependencies are correct (e.g., policy belongs to that state).

### Issue: Connection Refused
**Solution**: Make sure API server is running on port 8000.

---

## 📞 Support

For issues or questions about the API:
- Check Swagger UI: http://localhost:8000/docs
- Review this documentation
- Check API logs in terminal

---

## 🎯 Use Cases

### Use Case 1: Create Health Insurance Identifier
1. Get available states
2. Select state → Get policies
3. Select policy → Get plans
4. Select plan → Get programs
5. Select program → Get risk types
6. Select risk type → Get risk levels
7. Submit all data → Create identifier

### Use Case 2: Create Product Order
1. Get countries
2. Select country → Get cities
3. Get categories
4. Select category → Get products
5. Submit order data → Create order

---

**Last Updated**: October 31, 2025  
**Version**: 2.0.0  
**Purpose**: Testing Dynamic AI Agent System
