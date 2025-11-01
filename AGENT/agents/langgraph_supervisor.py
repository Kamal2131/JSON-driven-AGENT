from typing import Dict, Any, Optional, TypedDict, Literal
from langgraph.graph import StateGraph, END
from services.llm_service import LLMService
from services.tracing_service import tracing_service


class SupervisorState(TypedDict):
    """State for supervisor agent"""
    user_input: str
    available_workflows: Dict[str, Dict[str, Any]]
    selected_workflow: Optional[str]
    confidence: float
    reasoning: str


class LangGraphSupervisorAgent:
    """Supervisor agent using LangGraph for intelligent routing"""
    
    def __init__(self, llm_service: LLMService, available_workflows: Dict[str, Dict[str, Any]]):
        self.llm_service = llm_service
        self.available_workflows = available_workflows
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build supervisor routing graph"""
        workflow = StateGraph(SupervisorState)
        
        workflow.add_node("analyze_intent", self._analyze_intent_node)
        workflow.add_node("match_workflow", self._match_workflow_node)
        workflow.add_node("validate_match", self._validate_match_node)
        
        workflow.set_entry_point("analyze_intent")
        workflow.add_edge("analyze_intent", "match_workflow")
        
        workflow.add_conditional_edges(
            "match_workflow",
            self._check_confidence,
            {
                "high": "validate_match",
                "low": END
            }
        )
        
        workflow.add_edge("validate_match", END)
        
        return workflow.compile()
    
    @tracing_service.trace_function("analyze_intent")
    def _analyze_intent_node(self, state: SupervisorState) -> SupervisorState:
        """Analyze user intent"""
        user_input = state["user_input"]
        
        prompt = f"""Analyze this user request and extract the intent:
        
User: "{user_input}"

Identify:
1. Primary action (create, view, get, update, delete)
2. Target entity (identifier, policy, state, order, registration)
3. Key parameters mentioned

Return in format:
Action: <action>
Entity: <entity>
Parameters: <list>"""
        
        analysis = self.llm_service.generate(prompt)
        state["reasoning"] = analysis
        
        return state
    
    @tracing_service.trace_function("match_workflow")
    def _match_workflow_node(self, state: SupervisorState) -> SupervisorState:
        """Match to appropriate workflow"""
        workflow_descriptions = "\n".join([
            f"- {name}: {config.get('description', config.get('api_name', name))}"
            for name, config in state["available_workflows"].items()
        ])
        
        prompt = f"""Based on the user's request, select the most appropriate workflow.

User request: "{state['user_input']}"

Intent analysis: {state['reasoning']}

Available workflows:
{workflow_descriptions}

Return ONLY the exact workflow name that best matches. If no match, return "UNKNOWN"."""
        
        selected = self.llm_service.generate(prompt).strip()
        
        # Find exact or partial match
        matched_workflow = None
        max_confidence = 0.0
        
        for workflow_name in state["available_workflows"].keys():
            if workflow_name.lower() == selected.lower():
                matched_workflow = workflow_name
                max_confidence = 1.0
                break
            elif workflow_name.lower() in selected.lower() or selected.lower() in workflow_name.lower():
                matched_workflow = workflow_name
                max_confidence = 0.8
        
        state["selected_workflow"] = matched_workflow
        state["confidence"] = max_confidence
        
        return state
    
    def _validate_match_node(self, state: SupervisorState) -> SupervisorState:
        """Validate the matched workflow"""
        if state["selected_workflow"]:
            workflow_config = state["available_workflows"][state["selected_workflow"]]
            print(f"✅ Matched workflow: {state['selected_workflow']}")
            print(f"   Description: {workflow_config.get('description', 'N/A')}")
            print(f"   Confidence: {state['confidence']:.2%}")
        
        return state
    
    def _check_confidence(self, state: SupervisorState) -> Literal["high", "low"]:
        """Check if confidence is high enough"""
        return "high" if state.get("confidence", 0) >= 0.7 else "low"
    
    @tracing_service.trace_function("route_request")
    def route_request(self, user_input: str) -> Optional[str]:
        """Route user request to appropriate workflow"""
        initial_state: SupervisorState = {
            "user_input": user_input,
            "available_workflows": self.available_workflows,
            "selected_workflow": None,
            "confidence": 0.0,
            "reasoning": ""
        }
        
        final_state = self.graph.invoke(initial_state)
        
        return final_state.get("selected_workflow")
    
    @tracing_service.trace_function("generate_response")
    def generate_response(self, result: Dict[str, Any], workflow_name: str) -> str:
        """Generate human-readable response from API result"""
        if not result.get("success", True):
            return f"❌ Error: {result.get('message', result.get('error', 'Unknown error occurred'))}"
        
        prompt = f"""Convert this API response into a clear, structured message.

Workflow: {workflow_name}
Response: {result}

Format the response with:
- Clear sections using headers
- Key information in bullet points
- Important values highlighted
- Keep it concise and organized

Example format:
✅ Success!

📋 Enrollment Details:
  • ID: ENR123
  • State: Maharashtra
  • Plan: Silver

💰 Premium:
  • Base: ₹5,500
  • Total: ₹6,600

👤 Applicant: Name (email)"""
        
        return self.llm_service.generate(prompt)
