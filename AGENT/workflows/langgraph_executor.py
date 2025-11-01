from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from agents.parameter_collector_agent import ParameterCollectorAgent
from agents.api_executor_agent import APIExecutorAgent
from services.tracing_service import tracing_service
import os

class WorkflowState(TypedDict):
    config: Dict[str, Any]
    user_input: str
    collected_params: Dict[str, Any]
    api_response: Dict[str, Any]
    error: str
    iteration: int
    max_iterations: int

class LangGraphWorkflowExecutor:
    def __init__(self, parameter_collector: ParameterCollectorAgent, 
                 api_executor: APIExecutorAgent):
        self.parameter_collector = parameter_collector
        self.api_executor = api_executor
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        workflow = StateGraph(WorkflowState)
        
        workflow.add_node("collect_parameters", self._collect_parameters_node)
        workflow.add_node("execute_api", self._execute_api_node)
        workflow.add_node("handle_error", self._handle_error_node)
        
        workflow.set_entry_point("collect_parameters")
        
        workflow.add_conditional_edges(
            "collect_parameters",
            self._should_execute_api,
            {
                "execute": "execute_api",
                "error": "handle_error",
                "retry": "collect_parameters"
            }
        )
        
        workflow.add_conditional_edges(
            "execute_api",
            self._check_api_result,
            {
                "success": END,
                "error": "handle_error"
            }
        )
        
        workflow.add_edge("handle_error", END)
        return workflow.compile()
    
    @tracing_service.trace_function("collect_parameters_node")
    def _collect_parameters_node(self, state: WorkflowState) -> WorkflowState:
        try:
            print(f"\n📋 Collecting parameters (iteration {state.get('iteration', 0) + 1})...")
            collected_params = self.parameter_collector.collect_parameters(
                config=state["config"],
                user_input=state["user_input"],
                collected_params=state.get("collected_params", {})
            )
            state["collected_params"] = collected_params
            state["iteration"] = state.get("iteration", 0) + 1
            state["error"] = ""
            print(f"✅ Collected {len(collected_params)} parameters")
        except Exception as e:
            state["error"] = f"Parameter collection failed: {str(e)}"
            print(f"❌ {state['error']}")
        return state
    
    @tracing_service.trace_function("execute_api_node")
    def _execute_api_node(self, state: WorkflowState) -> WorkflowState:
        try:
            print("\n🚀 Executing API call...")
            api_response = self.api_executor.execute(
                config=state["config"],
                parameters=state["collected_params"]
            )
            state["api_response"] = api_response
            if not api_response.get("success", True):
                state["error"] = api_response.get("error", "API call failed")
        except Exception as e:
            state["error"] = f"API execution failed: {str(e)}"
            state["api_response"] = {"success": False, "error": str(e)}
            print(f"❌ {state['error']}")
        return state
    
    def _handle_error_node(self, state: WorkflowState) -> WorkflowState:
        print(f"\n⚠️  Error Handler: {state.get('error', 'Unknown error')}")
        return state
    
    def _should_execute_api(self, state: WorkflowState) -> str:
        if state.get("error"):
            return "error"
        
        config = state["config"]
        parameters = config.get("parameters", {})
        collected = state.get("collected_params", {})
        
        required_params = [
            name for name, conf in parameters.items() 
            if conf.get("required", False)
        ]
        
        missing = [p for p in required_params if p not in collected or collected[p] is None]
        
        if missing:
            if state.get("iteration", 0) >= state.get("max_iterations", 10):
                state["error"] = f"Could not collect required parameters: {missing}"
                return "error"
            return "retry"
        return "execute"
    
    def _check_api_result(self, state: WorkflowState) -> str:
        if state.get("error"):
            return "error"
        api_response = state.get("api_response", {})
        if not api_response.get("success", True):
            return "error"
        return "success"
    
    @tracing_service.trace_function("workflow_execute")
    def execute(self, config: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        initial_state: WorkflowState = {
            "config": config,
            "user_input": user_input,
            "collected_params": {},
            "api_response": {},
            "error": "",
            "iteration": 0,
            "max_iterations": 10
        }
        
        print("\n🔍 LangGraph execution will be traced in LangSmith...")
        final_state = self.graph.invoke(
            initial_state,
            config={"run_name": f"Workflow: {config.get('api_name', 'Unknown')}"}
        )
        
        return {
            "success": not final_state.get("error"),
            "collected_params": final_state.get("collected_params", {}),
            "api_response": final_state.get("api_response", {}),
            "error": final_state.get("error", "")
        }
