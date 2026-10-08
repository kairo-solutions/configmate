"""
ConfigMate - Advanced configuration management utility
"""

import os
import json
from typing import Any, Dict, Optional, Union, List, Callable
from pathlib import Path
import re


class ValidationError(Exception):
    """Raised when configuration validation fails."""
    pass


class Config:
    """An advanced configuration manager with validation and nested support."""
    
    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._defaults: Dict[str, Any] = {}
        self._type_hints: Dict[str, type] = {}
        self._validators: Dict[str, Callable[[Any], bool]] = {}
        self._required: set = set()
    
    def set_default(self, key: str, value: Any, type_hint: type = str) -> None:
        """Set a default value for a configuration key."""
        self._defaults[key] = value
        self._type_hints[key] = type_hint
        
        # If key doesn't exist, set it to the default
        if key not in self._config:
            self._config[key] = value
    
    def require(self, key: str) -> None:
        """Mark a configuration key as required."""
        self._required.add(key)
    
    def validate(self, key: str, validator: Callable[[Any], bool]) -> None:
        """Add a validation function for a configuration key."""
        self._validators[key] = validator
    
    def load_from_env(self, prefix: str = '', lowercase_keys: bool = True, 
                     separator: str = '__') -> None:
        """Load configuration from environment variables."""
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):]
                if lowercase_keys:
                    # Convert APP_DATABASE__HOST to database.host
                    config_key = config_key.lower()
                    if separator in config_key:
                        parts = config_key.split(separator)
                        config_key = '.'.join(part.lower() for part in parts)
                
                # Try to convert value to appropriate type
                converted_value = self._convert_value(config_key, value)
                self._set_nested(config_key, converted_value)
    
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
        
        self._update_nested(self._flatten_dict(data))
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value, supporting nested keys."""
        return self._get_nested(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value, supporting nested keys."""
        self._set_nested(key, value)
    
    def validate_all(self) -> List[str]:
        """Validate all configuration and return list of errors."""
        errors = []
        
        # Check required fields
        for key in self._required:
            if self._get_nested(key, None) is None:
                errors.append(f"Required configuration key missing: {key}")
        
        # Run validators
        for key, validator in self._validators.items():
            value = self._get_nested(key)
            if value is not None and not validator(value):
                errors.append(f"Validation failed for key '{key}': {value}")
        
        # Check type hints
        for key, expected_type in self._type_hints.items():
            value = self._get_nested(key)
            if value is not None and not isinstance(value, expected_type):
                errors.append(
                    f"Type mismatch for key '{key}': expected {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Return the entire configuration as a dictionary."""
        return self._config.copy()
    
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
    
    def _get_nested(self, key: str, default: Any = None) -> Any:
        """Get a nested configuration value using dot notation."""
        if '.' not in key:
            return self._config.get(key, default)
        
        parts = key.split('.')
        current = self._config
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current
    
    def _set_nested(self, key: str, value: Any) -> None:
        """Set a nested configuration value using dot notation."""
        if '.' not in key:
            self._config[key] = value
            return
        
        parts = key.split('.')
        current = self._config
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """Flatten a nested dictionary."""
        items: List[tuple] = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _update_nested(self, update_dict: Dict[str, Any]) -> None:
        """Update configuration with a flattened dictionary."""
        for key, value in update_dict.items():
            self._set_nested(key, value)


# Convenience instance
config = Config()
