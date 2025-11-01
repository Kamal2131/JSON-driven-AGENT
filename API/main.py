from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import states, policies, plans, risks, identifier, identifier_v2, dummy_endpoints

app = FastAPI(
    title="Health Insurance Enrollment API",
    description="REST APIs for dynamic form-filling system with interdependent data flow",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(states.router)
app.include_router(policies.router)
app.include_router(plans.router)
app.include_router(risks.router)
app.include_router(identifier.router)
app.include_router(identifier_v2.router)
app.include_router(dummy_endpoints.router)

@app.get("/")
def root():
    return {
        "message": "Dynamic AI Agent - Health Insurance API",
        "version": "2.0.0",
        "description": "Fully dynamic API supporting names or IDs for all endpoints",
        "endpoints": {
            "states": "/api/v1/states",
            "policies": "/api/v1/policies?state={state_name_or_id}",
            "plans": "/api/v1/plans?state={state}&policy={policy_name_or_id}",
            "programs": "/api/v1/plans/{plan_name_or_id}/programs",
            "risk_types": "/api/v1/programs/{program_name_or_id}/risk-types",
            "risk_levels": "/api/v1/risk-types/{risk_type_name_or_id}/risk-levels",
            "create_identifier": "/api/v1/identifier/create",
            "countries": "/api/v1/dummy/countries",
            "cities": "/api/v1/dummy/cities?country={country_name}",
            "categories": "/api/v1/dummy/categories",
            "products": "/api/v1/dummy/products?category={category_id}",
            "create_order": "/api/v1/dummy/orders/create",
            "create_registration": "/api/v1/dummy/registrations/create"
        },
        "examples": {
            "create_identifier": {
                "url": "/api/v1/identifier/create",
                "method": "POST",
                "body": {
                    "state": "Karnataka",
                    "policy": "Family Cover",
                    "plan": "Gold",
                    "program": "Wellness Plus",
                    "risk_type": "Low Risk",
                    "risk_level": "Tier 1",
                    "applicant_first_name": "John",
                    "applicant_last_name": "Doe",
                    "applicant_email": "john@example.com"
                }
            },
            "create_order": {
                "url": "/api/v1/dummy/orders/create",
                "method": "POST",
                "body": {
                    "country": "India",
                    "city": "Mumbai",
                    "category": "electronics",
                    "product": "P001",
                    "customer_name": "John Doe",
                    "customer_email": "john@example.com"
                }
            }
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
