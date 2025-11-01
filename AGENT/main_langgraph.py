import os
from pathlib import Path
from dotenv import load_dotenv
from services.llm_service import LLMServiceFactory
from services.api_service import HTTPAPIService
from agents.langgraph_supervisor import LangGraphSupervisorAgent
from agents.parameter_collector_agent import ParameterCollectorAgent
from agents.api_executor_agent import APIExecutorAgent
from workflows.langgraph_executor import LangGraphWorkflowExecutor
from utils.config_loader import ConfigLoader

# Load environment variables
load_dotenv()

# Initialize LangSmith tracing if enabled
if os.getenv("LANGSMITH_TRACING", "false").lower() == "true":
    try:
        from langsmith import Client
        langsmith_client = Client(
            api_key=os.getenv("LANGSMITH_API_KEY"),
            api_url=os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
        )
        print("✅ LangSmith tracing enabled")
        print(f"📊 Project: {os.getenv('LANGSMITH_PROJECT')}")
    except ImportError:
        print("⚠️  LangSmith not installed. Install with: pip install langsmith")


class DynamicAgentSystemV2:
    """Enhanced dynamic agent system with LangGraph integration"""
    
    def __init__(self, config_dir: str, base_url: str, llm_type: str = "openai"):
        # Initialize services (SOLID: Dependency Injection)
        self.llm_service = LLMServiceFactory.create(llm_type)
        self.api_service = HTTPAPIService(base_url=base_url)
        
        # Load all workflow configurations
        self.workflows = ConfigLoader.load_all_configs(config_dir)
        print(f"📚 Loaded {len(self.workflows)} workflow configurations")
        
        # Initialize agents
        self.supervisor = LangGraphSupervisorAgent(self.llm_service, self.workflows)
        self.parameter_collector = ParameterCollectorAgent(self.llm_service, self.api_service)
        self.api_executor = APIExecutorAgent(self.api_service)
        
        # Initialize LangGraph workflow executor
        self.workflow_executor = LangGraphWorkflowExecutor(
            self.parameter_collector, 
            self.api_executor
        )
    
    def process_request(self, user_input: str) -> str:
        """Process user request end-to-end using LangGraph"""
        print(f"\n{'='*60}")
        print(f"🤖 Processing: {user_input}")
        print(f"{'='*60}")
        
        # Step 1: Route to appropriate workflow using LangGraph supervisor
        workflow_name = self.supervisor.route_request(user_input)
        
        if not workflow_name:
            return "❌ I couldn't find a matching workflow for your request. Please try rephrasing."
        
        print(f"\n📋 Selected workflow: {workflow_name}")
        
        # Step 2: Get workflow config
        config = self.workflows[workflow_name]
        print(f"🔧 Method: {config.get('method')} {config.get('endpoint')}")
        
        # Step 3: Execute workflow using LangGraph
        result = self.workflow_executor.execute(config, user_input)
        
        if not result["success"]:
            return f"❌ Error: {result.get('error', 'Unknown error')}"
        
        # Step 4: Generate response
        response = self.supervisor.generate_response(result["api_response"], workflow_name)
        
        return response
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("=" * 60)
        print("🚀 Dynamic Agent System V2 (LangGraph Edition)")
        print("=" * 60)
        print(f"\n✨ Features:")
        print("  - LangGraph state management")
        print("  - Intelligent workflow routing")
        print("  - Dynamic parameter collection")
        print("  - Dependency resolution")
        print(f"\n📋 Available workflows ({len(self.workflows)}):")
        for name, config in self.workflows.items():
            method = config.get('method', 'GET')
            endpoint = config.get('endpoint', '')
            desc = config.get('description', 'No description')
            print(f"  - {name}")
            print(f"    {method} {endpoint}")
            print(f"    {desc}")
        print("\n💡 Examples:")
        print("  - 'I want to create an identifier for California'")
        print("  - 'Show me all available states'")
        print("  - 'Create an order for a laptop in India'")
        print("\nType 'exit' to quit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                response = self.process_request(user_input)
                print(f"\n🤖 Agent: {response}\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")


def main():
    """Main entry point"""
    # Configuration
    CONFIG_DIR = os.path.join(Path(__file__).parent, "config", "workflows")
    BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
    LLM_TYPE = os.getenv("LLM_TYPE", "openai")
    
    # Create config directory if it doesn't exist
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    # Initialize system
    system = DynamicAgentSystemV2(
        config_dir=CONFIG_DIR,
        base_url=BASE_URL,
        llm_type=LLM_TYPE
    )
    
    # Run interactive mode
    system.interactive_mode()


if __name__ == "__main__":
    main()
