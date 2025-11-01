from typing import Dict, Any, List, Optional
from services.llm_service import LLMService
from services.api_service import APIService
from services.tracing_service import tracing_service
from utils.json_path_extractor import JSONPathExtractor

class ParameterCollectorAgent:
    """Agent responsible for collecting parameters dynamically based on config"""
    
    def __init__(self, llm_service: LLMService, api_service: APIService):
        self.llm_service = llm_service
        self.api_service = api_service
    
    @tracing_service.trace_function("collect_parameters")
    def collect_parameters(self, config: Dict[str, Any], user_input: str, 
                          collected_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Collect all required parameters for the workflow"""
        if collected_params is None:
            collected_params = {}
        
        parameters = config.get("parameters", {})
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            params_collected_this_round = False
            
            for param_name, param_config in parameters.items():
                if param_name in collected_params:
                    continue
                
                # Check if parameter has api_call defined
                api_call = param_config.get("api_call")
                
                if api_call:
                    # Has API call - check dependencies
                    depends_on = param_config.get("depends_on")
                    if depends_on:
                        # Ensure dependencies are collected first
                        if isinstance(depends_on, str):
                            depends_on = [depends_on]
                        
                        if not all(dep in collected_params for dep in depends_on):
                            continue
                    
                    # Fetch options from API
                    options = self._fetch_dependent_options(param_config, collected_params)
                    
                    if options:
                        selected = self._llm_select_option(param_name, options, user_input)
                        collected_params[param_name] = selected
                        params_collected_this_round = True
                    elif not param_config.get("required", False):
                        # Optional param with no options - skip
                        params_collected_this_round = True
                else:
                    # No API call - extract from user input
                    value = self._extract_from_user_input(param_name, param_config, user_input)
                    if value:
                        collected_params[param_name] = value
                        params_collected_this_round = True
            
            # If no params collected this round, break
            if not params_collected_this_round:
                break
        
        return collected_params
    
    def _fetch_dependent_options(self, param_config: Dict[str, Any], 
                                 collected_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch options from dependent API call"""
        api_call = param_config.get("api_call")
        if not api_call:
            return []
        
        # Replace placeholders in API call (both path and query params)
        for key, value in collected_params.items():
            api_call = api_call.replace(f"{{{key}}}", str(value))
        
        # Parse query parameters
        if "?" in api_call:
            endpoint, query_string = api_call.split("?", 1)
            params = {}
            for param in query_string.split("&"):
                if "=" in param:
                    k, v = param.split("=", 1)
                    # Replace any remaining placeholders in values
                    for key, value in collected_params.items():
                        v = v.replace(f"{{{key}}}", str(value))
                    params[k] = v
        else:
            endpoint = api_call
            params = None
        
        try:
            response = self.api_service.get(endpoint, params=params)
            response_field = param_config.get("response_field", "data")
            display_field = param_config.get("display_field", response_field)
            
            # Extract options using JSONPathExtractor
            extracted_data = JSONPathExtractor.extract(response, response_field)
            
            # If display_field is different, extract that too
            display_data = extracted_data
            if display_field != response_field:
                display_data = JSONPathExtractor.extract(response, display_field)
            
            if isinstance(extracted_data, list):
                if isinstance(display_data, list) and len(display_data) == len(extracted_data):
                    return [{"label": str(display_data[i]), "value": extracted_data[i]} for i in range(len(extracted_data))]
                else:
                    return [{"label": str(item), "value": item} for item in extracted_data]
            
            return []
        except Exception as e:
            print(f"   ❌ Error fetching options from {endpoint}: {e}")
            return []
    
    def _llm_select_option(self, param_name: str, options: List[Dict[str, Any]], 
                          user_input: str) -> Any:
        """Ask user to select from options"""
        if not options:
            return None
        
        if len(options) == 1:
            print(f"   ℹ️  Only one option for {param_name}: {options[0]['label']}")
            return options[0]["value"]
        
        # Display options to user
        print(f"\n📋 Please select {param_name}:")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt['label']}")
        
        while True:
            try:
                choice = input(f"Enter choice (1-{len(options)}): ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    selected = options[idx]
                    print(f"   ✅ Selected {param_name}: {selected['label']}")
                    return selected["value"]
                else:
                    print(f"   ⚠️  Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("   ⚠️  Please enter a valid number")
            except KeyboardInterrupt:
                print("\n   ⚠️  Selection cancelled, using first option")
                return options[0]["value"]
    
    def _extract_from_user_input(self, param_name: str, param_config: Dict[str, Any], 
                                 user_input: str) -> Optional[str]:
        """Extract or ask user for parameter value"""
        param_type = param_config.get("type", "string")
        required = param_config.get("required", False)
        default_value = param_config.get("default")
        
        # Use default if provided
        if default_value is not None:
            return default_value
        
        # Try to extract from user input first
        prompt = f"""Extract the value for parameter "{param_name}" (type: {param_type}) from this user request:
"{user_input}"

If the value is not explicitly mentioned, return "NOT_FOUND".
Return ONLY the extracted value, nothing else."""
        
        value = self.llm_service.generate(prompt).strip().strip('"').strip("'")
        
        # If not found and required, ask user
        if value == "NOT_FOUND" and required:
            print(f"\n❓ Please provide {param_name} (type: {param_type}):")
            value = input(f"{param_name}: ").strip()
            if value:
                print(f"   ✅ Got {param_name}: {value}")
                return value
            return None
        
        return value if value != "NOT_FOUND" else None
