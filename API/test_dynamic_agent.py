"""
Test script to validate APIs for dynamic agent system
Run: python test_dynamic_agent.py
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_query_based_workflow():
    print("=" * 60)
    print("Testing Query-Based Workflow (Dynamic Agent Compatible)")
    print("=" * 60)
    
    # Step 1: Get states
    print("\n1. Fetching states...")
    response = requests.get(f"{BASE_URL}/states")
    states = response.json()
    print(f"Response: {json.dumps(states, indent=2)}")
    
    if states["success"] and states["data"]:
        state_name = states["data"][0]["state_name"]
        print(f"Selected State: {state_name}")
        
        # Step 2: Get policies by state
        print(f"\n2. Fetching policies for state: {state_name}")
        response = requests.get(f"{BASE_URL}/policies", params={"state": state_name})
        policies = response.json()
        print(f"Response: {json.dumps(policies, indent=2)}")
        
        if policies["success"] and policies["classPlanList"]:
            policy_name = policies["classPlanList"][0]["policy_name"]
            print(f"Selected Policy: {policy_name}")
            
            # Step 3: Get plans by state and policy
            print(f"\n3. Fetching plans for state: {state_name}, policy: {policy_name}")
            response = requests.get(f"{BASE_URL}/plans", params={"state": state_name, "policy": policy_name})
            plans = response.json()
            print(f"Response: {json.dumps(plans, indent=2)}")
            
            if plans["success"] and plans["classPlanList"]:
                plan_name = plans["classPlanList"][0]["plan_name"]
                print(f"Selected Plan: {plan_name}")
                
                # Step 4: Create identifier
                print(f"\n4. Creating identifier...")
                payload = {
                    "configuration_name": "test_config_001",
                    "state": state_name,
                    "policy": policy_name,
                    "plan": plan_name,
                    "applicant_first_name": "John",
                    "applicant_last_name": "Doe",
                    "applicant_email": "john.doe@example.com"
                }
                response = requests.post(f"{BASE_URL}/identifier/create", json=payload)
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
                
                if result["success"]:
                    print("\n✅ Workflow completed successfully!")
                    print(f"Enrollment ID: {result['data']['enrollment_id']}")
                    print(f"Identifier Code: {result['data']['identifier_code']}")
                else:
                    print("\n❌ Failed to create identifier")
            else:
                print("\n❌ No plans found")
        else:
            print("\n❌ No policies found")
    else:
        print("\n❌ No states found")

def test_response_field_extraction():
    print("\n" + "=" * 60)
    print("Testing Response Field Extraction")
    print("=" * 60)
    
    # Test classPlanList[].PolicyId extraction
    print("\n1. Testing classPlanList[].PolicyId extraction")
    response = requests.get(f"{BASE_URL}/policies", params={"state": "Gujarat"})
    data = response.json()
    
    if "classPlanList" in data:
        policy_ids = [item["PolicyId"] for item in data["classPlanList"]]
        print(f"Extracted PolicyIds: {policy_ids}")
    
    # Test classPlanList[].PlanDescription extraction
    print("\n2. Testing classPlanList[].PlanDescription extraction")
    response = requests.get(f"{BASE_URL}/plans", params={"state": "Gujarat", "policy": "Health Policy"})
    data = response.json()
    
    if "classPlanList" in data:
        plan_descriptions = [item["PlanDescription"] for item in data["classPlanList"]]
        print(f"Extracted PlanDescriptions: {plan_descriptions}")

if __name__ == "__main__":
    try:
        test_query_based_workflow()
        test_response_field_extraction()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("Make sure the server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
