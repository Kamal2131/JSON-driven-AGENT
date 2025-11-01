# Health Insurance API - Testing Backend

> ⚠️ **FOR TESTING PURPOSES ONLY**  
> This API provides test endpoints for the Dynamic AI Agent System.

---

## 🎯 Purpose

This FastAPI backend provides REST endpoints to test the Dynamic AI Agent System's ability to:
- Handle dependent API calls
- Extract dynamic response fields
- Manage cascading parameters
- Process complex workflows

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd API
pip install -r requirements.txt
```

### 2. Start Server
```bash
uvicorn main:app --reload --port 8000
```

### 3. Access Documentation
- **Swagger UI**: http://localhost:8000/docs
- **API Guide**: [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md)

---

## 📁 Project Structure

```
API/
├── main.py                    # FastAPI app entry point
├── routers/                   # API route handlers
│   ├── states.py             # State endpoints
│   ├── policies.py           # Policy endpoints
│   ├── plans.py              # Plan endpoints
│   ├── risks.py              # Risk type/level endpoints
│   ├── identifier.py         # Identifier creation (v1)
│   ├── identifier_v2.py      # Identifier creation (v2)
│   └── dummy_endpoints.py    # Test endpoints
├── utils/
│   └── data.py               # In-memory test data
├── models/
│   └── schemas.py            # Pydantic models
└── requirements.txt          # Dependencies
```

---

## 🔗 API Endpoints

### Health Insurance Workflow
```
GET  /api/v1/states                              # Get all states
GET  /api/v1/policies?state={state}              # Get policies by state
GET  /api/v1/plans?state={state}&policy={policy} # Get plans
GET  /api/v1/plans/{plan}/programs               # Get programs
GET  /api/v1/programs/{program}/risk-types       # Get risk types
GET  /api/v1/risk-types/{risk_type}/risk-levels  # Get risk levels
POST /api/v1/identifier/create                   # Create identifier
```

### Dummy Test Endpoints
```
GET  /api/v1/dummy/countries                     # Get countries
GET  /api/v1/dummy/cities?country={country}      # Get cities
GET  /api/v1/dummy/categories                    # Get categories
GET  /api/v1/dummy/products?category={category}  # Get products
POST /api/v1/dummy/orders/create                 # Create order
POST /api/v1/dummy/registrations/create          # Create registration
```

---

## 📊 Test Data

### Health Insurance Data
- **5 States**: Gujarat, Maharashtra, Karnataka, Tamil Nadu, Delhi
- **11 Policies**: Individual, Family, Corporate, Senior plans
- **17 Plans**: Gold, Silver, Platinum, Bronze tiers
- **15 Programs**: Wellness, Chronic Care, Maternity, Preventive
- **10 Risk Types**: Low, Medium, High risk categories
- **15 Risk Levels**: Tier 1, 2, 3 levels

### Dummy Data
- **Countries**: India, USA, UK, Canada, Australia
- **Cities**: Mumbai, Delhi, Bangalore, etc.
- **Categories**: Electronics, Clothing, Books
- **Products**: Laptops, Phones, Tablets

---

## 🧪 Example Usage

### Get States
```bash
curl http://localhost:8000/api/v1/states?active=true
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

---

## 🔑 Key Features

### 1. Flexible Input
Accepts both **names** and **IDs**:
```json
"state": "Gujarat"     // ✅ Works
"state": "ST001"       // ✅ Also works
```

### 2. Dependent Data
Cascading dependencies:
```
State → Policy → Plan → Program → Risk Type → Risk Level
```

### 3. Dynamic Response Fields
Responses use different field structures:
```json
// States endpoint
{"data": [...]}

// Policies endpoint
{"classPlanList": [...]}

// Plans endpoint
{"classPlanList": [...]}
```

### 4. CORS Enabled
All origins allowed for testing.

---

## ⚠️ Important Notes

1. **In-Memory Data**: All data stored in memory. Resets on restart.
2. **No Database**: No persistence. For testing only.
3. **No Authentication**: Open access for testing.
4. **Case Sensitive**: Names are case-sensitive.

---

## 📖 Documentation

- **Full API Guide**: [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md)
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104+
- **Python**: 3.10+
- **Validation**: Pydantic
- **CORS**: Enabled for all origins

---

## 📦 Dependencies

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

---

## 🔧 Configuration

No configuration needed. All settings are defaults:
- **Host**: 0.0.0.0
- **Port**: 8000
- **Reload**: Enabled in dev mode

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### CORS Issues
CORS is already enabled for all origins. No action needed.

---

## 🎯 Testing with Agent

This API is designed to work with the Dynamic AI Agent System:

1. Start this API server
2. Start the Agent system (see `AGENT/README.md`)
3. Agent will automatically call these endpoints
4. Test various workflows

---

## 📞 Support

For issues:
1. Check [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md)
2. Review Swagger UI at http://localhost:8000/docs
3. Check terminal logs

---

**Version**: 2.0.0  
**Purpose**: Testing Dynamic AI Agent System  
**Status**: Development/Testing Only
