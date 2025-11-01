import os
from typing import Dict, Any
from functools import wraps

class TracingService:
    def __init__(self):
        self.enabled = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
        self.client = None
        
        if self.enabled:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
            os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "default")
            os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
            
            try:
                from langsmith import Client
                self.client = Client(
                    api_key=os.getenv("LANGSMITH_API_KEY"),
                    api_url=os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
                )
            except ImportError:
                self.enabled = False
    
    def trace_function(self, name: str = None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if self.enabled and self.client:
                    try:
                        from langsmith import traceable
                        traced = traceable(name=name or func.__name__)(func)
                        return traced(*args, **kwargs)
                    except Exception:
                        pass
                return func(*args, **kwargs)
            return wrapper
        return decorator

tracing_service = TracingService()
