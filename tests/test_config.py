"""
Tests for ConfigMate
"""

import tempfile
import os
import json
from pathlib import Path
from configmate.config import Config


def test_set_default():
    """Test setting default values."""
    config = Config()
    config.set_default('test_key', 'default_value', str)
    assert config.get('test_key') == 'default_value'
    
    config.set_default('test_int', 42, int)
    assert config.get('test_int') == 42
    
    config.set_default('test_bool', True, bool)
    assert config.get('test_bool') is True


def test_load_from_env():
    """Test loading from environment variables."""
    # Set test environment variables
    os.environ['APP_DEBUG'] = 'true'
    os.environ['APP_PORT'] = '8080'
    os.environ['APP_NAME'] = 'myapp'
    
    config = Config()
    config.set_default('debug', False, bool)
    config.set_default('port', 0, int)
    config.set_default('name', '', str)
    
    config.load_from_env(prefix='APP_')
    
    assert config.get('debug') is True
    assert config.get('port') == 8080
    assert config.get('name') == 'myapp'
    
    # Clean up
    del os.environ['APP_DEBUG']
    del os.environ['APP_PORT']
    del os.environ['APP_NAME']


def test_load_from_file():
    """Test loading from JSON file."""
    config = Config()
    config.set_default('debug', False, bool)
    config.set_default('port', 0, int)
    
    # Create temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({'debug': True, 'port': 3000}, f)
        temp_file = f.name
    
    try:
        config.load_from_file(temp_file)
        assert config.get('debug') is True
        assert config.get('port') == 3000
    finally:
        os.unlink(temp_file)


def test_get_with_default():
    """Test getting values with fallback defaults."""
    config = Config()
    config.set_default('existing_key', 'default', str)
    
    # Should return the default since it was set
    assert config.get('existing_key') == 'default'
    
    # Should return provided default for unset key
    assert config.get('unset_key', 'provided_default') == 'provided_default'
    
    # Should return None for unset key with no default
    assert config.get('unset_key') is None


def test_set_and_get():
    """Test setting and getting values."""
    config = Config()
    config.set('test_key', 'test_value')
    assert config.get('test_key') == 'test_value'
    
    config.set('test_key', 'new_value')
    assert config.get('test_key') == 'new_value'


if __name__ == '__main__':
    test_set_default()
    test_load_from_env()
    test_load_from_file()
    test_get_with_default()
    test_set_and_get()
    print("All tests passed!")
