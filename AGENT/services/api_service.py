import requests
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class APIService(ABC):
    @abstractmethod
    def call(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        pass

class HTTPAPIService(APIService):
    def __init__(self, base_url: str = "", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
    
    def call(self, method: str, url: str, params: Optional[Dict] = None, 
             json: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        full_url = f"{self.base_url}{url}" if not url.startswith("http") else url
        response = self.session.request(
            method=method.upper(),
            url=full_url,
            params=params,
            json=json,
            headers=headers or {},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get(self, url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        return self.call("GET", url, params=params)
    
    def post(self, url: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self.call("POST", url, json=json)
    
    def put(self, url: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self.call("PUT", url, json=json)
    
    def patch(self, url: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self.call("PATCH", url, json=json)
    
    def delete(self, url: str) -> Dict[str, Any]:
        return self.call("DELETE", url)
