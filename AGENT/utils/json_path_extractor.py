from typing import Any, List, Dict
import re

class JSONPathExtractor:
    """Extract values from JSON using path notation like data[].field or data.field"""
    
    @staticmethod
    def extract(data: Any, path: str) -> Any:
        """
        Extract value from JSON using path notation
        Examples:
            data[].state_name -> extracts state_name from array in data
            classPlanList[].PolicyId -> extracts PolicyId from classPlanList array
            data.enrollment_id -> extracts enrollment_id from data object
        """
        if not path:
            return data
        
        parts = JSONPathExtractor._parse_path(path)
        current = data
        
        for part in parts:
            if part["type"] == "array":
                if isinstance(current, dict) and part["key"] in current:
                    current = current[part["key"]]
                    if isinstance(current, list):
                        if part["field"]:
                            current = [item.get(part["field"]) for item in current if isinstance(item, dict)]
                        continue
                return None
            elif part["type"] == "object":
                if isinstance(current, dict):
                    current = current.get(part["key"])
                else:
                    return None
        
        return current
    
    @staticmethod
    def _parse_path(path: str) -> List[Dict[str, Any]]:
        """Parse path string into structured parts"""
        parts = []
        segments = path.split(".")
        
        for segment in segments:
            if "[]" in segment:
                key = segment.replace("[]", "")
                parts.append({"type": "array", "key": key, "field": None})
            else:
                if parts and parts[-1]["type"] == "array" and parts[-1]["field"] is None:
                    parts[-1]["field"] = segment
                else:
                    parts.append({"type": "object", "key": segment})
        
        return parts
    
    @staticmethod
    def extract_options(data: Any, path: str, display_field: str = None, value_field: str = None) -> List[Dict[str, Any]]:
        """
        Extract options for dropdown/select from API response
        Returns list of {label, value} dicts
        """
        extracted = JSONPathExtractor.extract(data, path)
        
        if not extracted:
            return []
        
        if isinstance(extracted, list):
            if all(isinstance(item, dict) for item in extracted):
                return [
                    {
                        "label": item.get(display_field, str(item)) if display_field else str(item),
                        "value": item.get(value_field, item) if value_field else item
                    }
                    for item in extracted
                ]
            else:
                return [{"label": str(item), "value": item} for item in extracted]
        
        return [{"label": str(extracted), "value": extracted}]
