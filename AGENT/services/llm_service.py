from abc import ABC, abstractmethod
from typing import Dict, Any
import os
from functools import wraps

class LLMService(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        pass

def trace_llm_call(func):
    @wraps(func)
    def wrapper(self, prompt: str, **kwargs):
        if os.getenv("LANGSMITH_TRACING", "false").lower() == "true":
            try:
                from langsmith import traceable
                traced_func = traceable(name=f"{self.__class__.__name__}.{func.__name__}")(func)
                return traced_func(self, prompt, **kwargs)
            except ImportError:
                pass
        return func(self, prompt, **kwargs)
    return wrapper

class OpenAIService(LLMService):
    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model
    
    @trace_llm_call
    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    
    @trace_llm_call
    def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        import json
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

class LLMServiceFactory:
    @staticmethod
    def create(service_type: str = "openai", **kwargs) -> LLMService:
        if service_type == "openai":
            return OpenAIService(**kwargs)
        raise ValueError(f"Unknown service type: {service_type}")
