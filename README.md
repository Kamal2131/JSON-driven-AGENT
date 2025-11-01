# Dynamic AI Agent System

JSON-driven AI agent system using LangGraph and OpenAI that executes workflows without hardcoding.

## Project Structure

```
task14/
├── API/              # FastAPI backend with health insurance & dummy endpoints
├── AGENT/            # LangGraph AI agent system
├── JSON/             # Additional JSON configurations
└── .gitignore        # Git ignore rules
```

## Quick Start

### 1. Start API Server
```bash
cd API
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Run Agent System
```bash
cd AGENT
pip install -r requirements.txt
python main_langgraph.py
```

## Features

- **100% Configuration-Driven**: Add workflows by dropping JSON files
- **LangGraph State Machine**: Visual workflow execution
- **Dynamic Parameter Collection**: Smart dependency resolution
- **LangSmith Tracing**: Full observability
- **REST API Backend**: Health insurance + dummy test endpoints

## Documentation

- [API Documentation](API/README.md)
- [Agent Documentation](AGENT/README.md)
- [Workflow Configuration Guide](AGENT/config/workflows/README.md)

## Environment Setup

Copy `.env.example` to `.env` in AGENT folder and add your keys:
```
OPENAI_API_KEY=your_key
LANGSMITH_API_KEY=your_key
```

## Tech Stack

- **Backend**: FastAPI, Python 3.10+
- **Agent**: LangGraph, OpenAI, LangSmith
- **Architecture**: SOLID principles, Factory pattern
