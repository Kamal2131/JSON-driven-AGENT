import json
from typing import Dict, Any, List
from pathlib import Path

class ConfigLoader:
    """Load and parse workflow configuration files"""
    
    @staticmethod
    def load(config_path: str) -> Dict[str, Any]:
        """Load JSON configuration file"""
        with open(config_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def load_all_configs(config_dir: str) -> Dict[str, Dict[str, Any]]:
        """Load all JSON configs from directory"""
        configs = {}
        config_path = Path(config_dir)
        
        for json_file in config_path.glob("*.json"):
            config = ConfigLoader.load(str(json_file))
            config_name = config.get("api_name", json_file.stem)
            configs[config_name] = config
        
        return configs
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate configuration structure"""
        required_fields = ["api_name", "endpoint", "method"]
        return all(field in config for field in required_fields)
