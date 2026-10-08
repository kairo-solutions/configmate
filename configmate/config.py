"""
ConfigMate - Configuration management utility
"""

import os
import json
from typing import Any, Dict, Optional, Union
from pathlib import Path


class Config:
    """A simple configuration manager."""
    
    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._defaults: Dict[str, Any] = {}
        self._type_hints: Dict[str, type] = {}
    
    def set_default(self, key: str, value: Any, type_hint: type = str) -> None:
        """Set a default value for a configuration key."""
        self._defaults[key] = value
        self._type_hints[key] = type_hint
        
        # If key doesn't exist, set it to the default
        if key not in self._config:
            self._config[key] = value
    
    def load_from_env(self, prefix: str = '', lowercase_keys: bool = True) -> None:
        """Load configuration from environment variables."""
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):]
                if lowercase_keys:
                    config_key = config_key.lower().replace('__', '.')
                
                # Try to convert value to appropriate type
                converted_value = self._convert_value(config_key, value)
                self._config[config_key] = converted_value
    
    def load_from_file(self, file_path: Union[str, Path]) -> None:
        """Load configuration from a JSON or YAML file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        if path.suffix.lower() in ['.json', '.jsonc']:
            with open(path, 'r') as f:
                data = json.load(f)
        elif path.suffix.lower() in ['.yaml', '.yml']:
            try:
                import yaml
                with open(path, 'r') as f:
                    data = yaml.safe_load(f)
            except ImportError:
                raise ImportError("PyYAML is required to load YAML files")
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        
        self._config.update(self._flatten_dict(data))
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, self._defaults.get(key, default))
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value
    
    def _convert_value(self, key: str, value: str) -> Any:
        """Convert string value to appropriate type based on type hints."""
        if key in self._type_hints:
            type_hint = self._type_hints[key]
            try:
                if type_hint == bool:
                    return value.lower() in ('true', '1', 'yes', 'on')
                elif type_hint == int:
                    return int(value)
                elif type_hint == float:
                    return float(value)
                elif type_hint == list:
                    return json.loads(value)
                elif type_hint == dict:
                    return json.loads(value)
                else:
                    return type_hint(value)
            except (ValueError, json.JSONDecodeError):
                # If conversion fails, return as string
                return value
        return value
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """Flatten a nested dictionary."""
        items: List[Tuple[str, Any]] = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)


# Convenience instance
config = Config()
