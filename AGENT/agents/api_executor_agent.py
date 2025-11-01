from typing import Dict, Any
from services.api_service import APIService
from services.tracing_service import tracing_service

class APIExecutorAgent:
    """Agent responsible for executing API calls based on collected parameters"""
    
    def __init__(self, api_service: APIService):
        self.api_service = api_service
    
    @tracing_service.trace_function("execute_api")
    def execute(self, config: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the API call with collected parameters"""
        method = config.get("method", "GET").upper()
        endpoint = config.get("endpoint", "")
        
        # Replace path parameters
        for key, value in parameters.items():
            endpoint = endpoint.replace(f"{{{key}}}", str(value))
        
        # Separate query and body parameters
        query_params = {}
        body_params = {}
        
        param_configs = config.get("parameters", {})
        for param_name, param_value in parameters.items():
            param_config = param_configs.get(param_name, {})
            param_location = param_config.get("location", "body")
            
            if param_location == "query":
                query_params[param_name] = param_value
            elif param_location == "path":
                continue  # Already handled above
            else:
                body_params[param_name] = param_value
        
        # Execute based on method
        try:
            print(f"\n🔧 Executing {method} {endpoint}")
            print(f"📦 Query params: {query_params}")
            print(f"📦 Body params: {body_params}")
            
            if method == "GET":
                result = self.api_service.get(endpoint, params=query_params if query_params else None)
            elif method == "POST":
                result = self.api_service.post(endpoint, json=body_params if body_params else parameters)
            elif method == "PUT":
                result = self.api_service.put(endpoint, json=body_params if body_params else parameters)
            elif method == "PATCH":
                result = self.api_service.patch(endpoint, json=body_params if body_params else parameters)
            elif method == "DELETE":
                result = self.api_service.delete(endpoint)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            print(f"✅ API call successful")
            return result
            
        except Exception as e:
            print(f"❌ API call failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to execute {method} {endpoint}"
            }
