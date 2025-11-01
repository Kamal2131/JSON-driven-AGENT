# Dynamic AI Agent System

A fully dynamic, configuration-driven AI agent system built with LangGraph and OpenAI that can execute any API workflow without hardcoding.

## 🎯 Key Features

- **100% Dynamic**: No hardcoded workflows - everything driven by JSON configs
- **SOLID Principles**: Decoupled services, easy to extend and maintain
- **Multi-LLM Support**: Switch between OpenAI and Azure OpenAI by changing one config
- **Automatic Parameter Collection**: Intelligently collects parameters based on dependencies
- **Supervisor Agent**: Routes user requests to appropriate workflows
- **LangGraph State Machine**: Robust workflow execution with state management

## 🏗️ Architecture

```
AGENT/
├── services/           # Service layer (SOLID: Single Responsibility)
│   ├── llm_service.py     # LLM abstraction (OpenAI/Azure)
│   └── api_service.py     # HTTP API client
├── agents/            # Agent layer
│   ├── supervisor_agent.py         # Routes requests
│   ├── parameter_collector_agent.py # Collects parameters
│   └── api_executor_agent.py       # Executes APIs
├── workflows/         # Workflow orchestration
│   └── workflow_executor.py        # LangGraph state machine
├── utils/            # Utilities
│   ├── json_path_extractor.py     # Extract from JSON responses
│   └── config_loader.py           # Load workflow configs
├── config/
│   └── workflows/    # JSON workflow configurations
└── main.py          # Entry point
```

## 🚀 Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

3. **Start the API server (in another terminal):**
```bash
cd ../API
uvicorn main:app --reload
```

4. **Run the agent:**
```bash
python main.py
```

## 📝 Creating Workflow Configurations

Add JSON files to `config/workflows/` directory:

```json
{
  "api_name": "Create Identifier",
  "endpoint": "/identifier/create",
  "method": "POST",
  "description": "Create an enrollment identifier",
  "parameters": {
    "state": {
      "type": "string",
      "required": true,
      "location": "body"
    },
    "policy": {
      "type": "string",
      "required": true,
      "location": "body",
      "depends_on": "state",
      "api_call": "/policies?state={state}",
      "response_field": "classPlanList[].policy_name"
    }
  }
}
```

### Configuration Fields

- **api_name**: Unique workflow name
- **endpoint**: API endpoint path
- **method**: HTTP method (GET, POST, PUT, PATCH, DELETE)
- **description**: What the workflow does
- **parameters**: Object defining all parameters
  - **type**: Data type (string, integer, boolean, etc.)
  - **required**: Whether parameter is mandatory
  - **location**: Where parameter goes (body, query, path)
  - **depends_on**: Parameter(s) this depends on
  - **api_call**: API to fetch options from
  - **response_field**: JSON path to extract values

### Response Field Notation

- `data[]` - Array in data field
- `data[].field_name` - Extract field_name from array
- `classPlanList[].PolicyId` - Extract PolicyId from classPlanList
- `data.enrollment_id` - Direct field access

## 💡 Usage Examples

### Example 1: Create Identifier
```
You: I want to create an identifier for Gujarat with Health Policy and Gold plan
```

### Example 2: View States
```
You: Show me all available states
```

### Example 3: Get Policies
```
You: What policies are available in Maharashtra?
```

## 🔧 Switching LLM Providers

### Use OpenAI (default)
```bash
# .env
LLM_TYPE=openai
OPENAI_API_KEY=your_key
```

### Use Azure OpenAI
```bash
# .env
LLM_TYPE=azure
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment
```

## 🎨 SOLID Principles Applied

1. **Single Responsibility**: Each class has one job
   - `LLMService`: Only handles LLM calls
   - `APIService`: Only handles HTTP requests
   - `ParameterCollectorAgent`: Only collects parameters

2. **Open/Closed**: Extend without modifying
   - Add new LLM providers by extending `LLMService`
   - Add new workflows by adding JSON files

3. **Liskov Substitution**: Implementations are interchangeable
   - `OpenAIService` and `AzureOpenAIService` both implement `LLMService`

4. **Interface Segregation**: Focused interfaces
   - `LLMService` has only essential methods

5. **Dependency Inversion**: Depend on abstractions
   - Agents depend on `LLMService` interface, not concrete implementations

## 🧪 Testing

```bash
# Test with sample workflow
python main.py

# In the interactive prompt:
You: I want to create an identifier
```

## 📦 Adding New Workflows

1. Create JSON config in `config/workflows/`
2. Restart the agent
3. The supervisor will automatically detect and route to it

No code changes needed! 🎉

## 🔍 How It Works

1. **User Input** → Supervisor Agent
2. **Supervisor** → Selects appropriate workflow config
3. **Parameter Collector** → Gathers required parameters
   - Fetches dependent options from APIs
   - Uses LLM to select from options
4. **API Executor** → Calls the final API
5. **Supervisor** → Generates human-readable response

## 🛠️ Extending the System

### Add New LLM Provider
```python
class CustomLLMService(LLMService):
    def generate(self, prompt: str, **kwargs) -> str:
        # Your implementation
        pass
```

### Add New API Client
```python
class GraphQLAPIService(APIService):
    def call(self, method: str, url: str, **kwargs):
        # Your GraphQL implementation
        pass
```

## 📄 License

MIT
