# Dynamic AI Agent System

A fully dynamic, configuration-driven AI agent system built with LangGraph and OpenAI that can execute any API workflow without hardcoding.

## 🎯 Key Features

- **100% Dynamic**: No hardcoded workflows - everything driven by JSON configs
- **SOLID Principles**: Decoupled services, easy to extend and maintain
- **Multi-LLM Support**: Switch between OpenAI and Azure OpenAI by changing one config
- **Automatic Parameter Collection**: Intelligently collects parameters based on dependencies
- **Supervisor Agent**: Routes user requests to appropriate workflows using LangGraph
- **LangGraph State Machines**: Robust workflow execution with retry logic and error handling
- **LangSmith Tracing**: Full observability of all operations

## 🏗️ Architecture

```
AGENT/
├── services/                      # Service layer (SOLID)
│   ├── llm_service.py            # LLM abstraction (OpenAI/Azure)
│   ├── api_service.py            # HTTP API client
│   └── tracing_service.py        # LangSmith tracing
├── agents/                        # Agent layer
│   ├── langgraph_supervisor.py   # Routes requests (LangGraph)
│   ├── parameter_collector_agent.py # Collects parameters
│   └── api_executor_agent.py     # Executes APIs
├── workflows/                     # Workflow orchestration
│   └── langgraph_executor.py     # LangGraph state machine
├── utils/                         # Utilities
│   ├── json_path_extractor.py    # Extract from JSON responses
│   └── config_loader.py          # Load workflow configs
├── config/
│   └── workflows/                # JSON workflow configurations
└── main_langgraph.py             # Entry point
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd AGENT
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and add your keys:
```bash
OPENAI_API_KEY=your_openai_key
LANGSMITH_API_KEY=your_langsmith_key  # Optional
LANGSMITH_TRACING=true                # Optional
```

### 3. Start API Server (Terminal 1)
```bash
cd API
uvicorn main:app --reload --port 8000
```

### 4. Run Agent (Terminal 2)
```bash
cd AGENT
python main_langgraph.py
```

## 📝 Creating Workflow Configurations

Add JSON files to `config/workflows/` directory:

```json
{
  "api_name": "Create Identifier Enhanced",
  "endpoint": "/identifier/create",
  "method": "POST",
  "description": "Create health insurance identifier with dependent dropdowns",
  "parameters": {
    "state": {
      "type": "select",
      "label": "Select State",
      "required": true,
      "location": "body",
      "api_call": "/states?active=true",
      "response_field": "data[].state_name",
      "display_field": "data[].state_name"
    },
    "policy": {
      "type": "select",
      "label": "Select Policy",
      "required": true,
      "location": "body",
      "depends_on": "state",
      "api_call": "/policies?state={state}",
      "response_field": "classPlanList[].policy_name",
      "display_field": "classPlanList[].policy_name"
    },
    "applicant_first_name": {
      "type": "string",
      "label": "First Name",
      "required": true,
      "location": "body"
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
  - **type**: Data type (string, select, integer, boolean)
  - **label**: User-friendly label for the parameter
  - **required**: Whether parameter is mandatory
  - **location**: Where parameter goes (body, query, path)
  - **depends_on**: Parameter(s) this depends on (string or array)
  - **api_call**: API to fetch dropdown options from
  - **response_field**: JSON path to extract values
  - **display_field**: JSON path for display labels
  - **default**: Default value if not provided

### JSON Path Notation

- `data[].state_name` - Extract state_name from array in data
- `classPlanList[].policy_name` - Extract policy_name from classPlanList array
- `data.enrollment_id` - Direct field access
- `response.nested.field` - Deep nested field access

### Parameter Dependencies

```json
"depends_on": "state"              // Single dependency
"depends_on": ["state", "policy"]  // Multiple dependencies
```

Parameters wait for dependencies to be collected before fetching options.

## 💡 Usage Examples

### Example 1: Create Identifier
```
You: Create identifier

# Agent will:
# 1. Show state dropdown (Gujarat, Maharashtra, etc.)
# 2. Show policy dropdown based on selected state
# 3. Show plan dropdown based on selected policy
# 4. Show program dropdown based on selected plan
# 5. Ask for applicant details
# 6. Create identifier via API
# 7. Show formatted response
```

### Example 2: View States
```
You: Show me all states

# Agent calls GET /states and displays results
```

### Example 3: Create Order
```
You: Create an order

# Agent will guide through:
# Country → City → Category → Product → Customer details
```

## 🔧 Configuration Options

### LLM Provider

**OpenAI (default):**
```bash
LLM_TYPE=openai
OPENAI_API_KEY=your_key
```

**Azure OpenAI:**
```bash
LLM_TYPE=azure
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment
```

### LangSmith Tracing (Optional)

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=your_project_name
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

View traces at: https://smith.langchain.com

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
# Run the agent
python main_langgraph.py

# Try these commands:
You: Create identifier
You: Show me all states
You: Create an order
You: exit
```

## 📦 Adding New Workflows

1. Create JSON file in `config/workflows/`
2. Restart the agent
3. System automatically loads and routes to it

**No code changes needed!** 🎉

### Available Workflows

- `create_identifier_enhanced.json` - Health insurance identifier
- `create_full_enrollment.json` - Complete enrollment
- `create_order.json` - Product order
- `create_registration.json` - User registration
- `get_states.json` - View states
- `view_countries.json` - View countries
- `view_cities.json` - View cities

## 🔍 How It Works

### Flow Diagram
```
User Input
    ↓
[Supervisor LangGraph]
  ├─ Analyze Intent
  ├─ Match Workflow
  └─ Validate Match
    ↓
[Workflow Executor LangGraph]
  ├─ Collect Parameters (with retry)
  │   ├─ Fetch options from APIs
  │   ├─ Show dropdowns
  │   └─ Resolve dependencies
  ├─ Execute API
  └─ Handle Errors
    ↓
[Supervisor]
  └─ Generate Structured Response
    ↓
User sees formatted output
```

### Key Components

1. **Supervisor Agent** (LangGraph)
   - Analyzes user intent
   - Matches to workflow config
   - Generates responses

2. **Parameter Collector**
   - Reads JSON config
   - Resolves dependencies
   - Fetches dropdown options from APIs
   - Collects user input

3. **API Executor**
   - Builds request from collected params
   - Executes HTTP calls
   - Returns response

4. **Workflow Executor** (LangGraph)
   - State machine orchestration
   - Retry logic
   - Error handling

## 🛠️ Extending the System

### Add New LLM Provider
```python
# In services/llm_service.py
class ClaudeLLMService(LLMService):
    def generate(self, prompt: str, **kwargs) -> str:
        # Your Claude implementation
        pass

# In LLMServiceFactory
elif service_type == "claude":
    return ClaudeLLMService(**kwargs)
```

### Add New API Client
```python
# In services/api_service.py
class GraphQLAPIService(APIService):
    def call(self, method: str, url: str, **kwargs):
        # Your GraphQL implementation
        pass
```

### Add Custom Agent
```python
# In agents/
class CustomAgent:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    def process(self, state: Dict) -> Dict:
        # Your logic
        return state
```

## 📚 Documentation

- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **LangSmith Guide**: [LANGSMITH_GUIDE.md](LANGSMITH_GUIDE.md)
- **Setup Guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Workflow Config**: [config/workflows/README.md](config/workflows/README.md)

## 🐛 Troubleshooting

### Agent can't find workflow
- Check JSON file is in `config/workflows/`
- Verify JSON syntax is valid
- Restart the agent

### API connection failed
- Ensure API server is running on port 8000
- Check `API_BASE_URL` in `.env`

### LLM errors
- Verify `OPENAI_API_KEY` is set correctly
- Check API key has sufficient credits

## 📄 License

MIT
