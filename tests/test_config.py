"""
Tests for ConfigMate
"""

import tempfile
import os
import json
from pathlib import Path
from configmate.config import Config, ValidationError


def test_set_default():
    """Test setting default values."""
    config = Config()
    config.set_default('test_key', 'default_value', str)
    assert config.get('test_key') == 'default_value'
    
    config.set_default('test_int', 42, int)
    assert config.get('test_int') == 42
    
    config.set_default('test_bool', True, bool)
    assert config.get('test_bool') is True

    config.set_default('database.port', 5432, int)
    assert config.get('database.port') == 5432
    assert config.to_dict()['database']['port'] == 5432
    config.set('database.port', 6432)
    config.set_default('database.port', 5432, int)
    assert config.get('database.port') == 6432


def test_load_from_env():
    """Test loading from environment variables."""
    # Set test environment variables
    os.environ['APP_DEBUG'] = 'true'
    os.environ['APP_PORT'] = '8080'
    os.environ['APP_NAME'] = 'myapp'
    os.environ['APP_DATABASE__HOST'] = 'localhost'
    os.environ['APP_DATABASE__PORT'] = '5432'
    
    config = Config()
    config.set_default('debug', False, bool)
    config.set_default('port', 0, int)
    config.set_default('name', '', str)
    config.set_default('database.host', '', str)
    config.set_default('database.port', 0, int)
    
    config.load_from_env(prefix='APP_')
    
    assert config.get('debug') is True
    assert config.get('port') == 8080
    assert config.get('name') == 'myapp'
    assert config.get('database.host') == 'localhost'
    assert config.get('database.port') == 5432
    
    # Clean up
    del os.environ['APP_DEBUG']
    del os.environ['APP_PORT']
    del os.environ['APP_NAME']
    del os.environ['APP_DATABASE__HOST']
    del os.environ['APP_DATABASE__PORT']


def test_load_from_file():
    """Test loading from JSON file."""
    config = Config()
    config.set_default('debug', False, bool)
    config.set_default('port', 0, int)
    config.set_default('database.host', '', str)
    config.set_default('database.port', 0, int)
    
    # Create temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'debug': True, 
            'port': 3000,
            'database': {
                'host': 'prod-server',
                'port': 5432
            }
        }, f)
        temp_file = f.name
    
    try:
        config.load_from_file(temp_file)
        assert config.get('debug') is True
        assert config.get('port') == 3000
        assert config.get('database.host') == 'prod-server'
        assert config.get('database.port') == 5432
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
    
    # Test nested setting
    config.set('nested.key', 'nested_value')
    assert config.get('nested.key') == 'nested_value'
    assert config.get('nested') == {'key': 'nested_value'}


def test_required_fields():
    """Test required field validation."""
    config = Config()
    config.set_default('optional_key', 'default', str)
    config.require('required_key')
    config.require('another_required')
    
    # Should have errors for missing required fields
    errors = config.validate_all()
    assert len(errors) == 2
    assert any('required_key' in err for err in errors)
    assert any('another_required' in err for err in errors)
    
    # Set one required field
    config.set('required_key', 'value')
    errors = config.validate_all()
    assert len(errors) == 1
    assert 'another_required' in errors[0]
    
    # Set both required fields
    config.set('another_required', 'value')
    errors = config.validate_all()
    assert len(errors) == 0


def test_custom_validators():
    """Test custom validation functions."""
    config = Config()
    config.set_default('port', 8080, int)
    config.set_default('email', '', str)
    config.set_default('username', '', str)
    
    # Add validators
    config.validate('port', lambda x: 1 <= x <= 65535)
    config.validate('email', lambda x: '@' in x and '.' in x.split('@')[1])
    config.validate('username', lambda x: len(x) >= 3)
    
    # Test valid values
    config.set('port', 3000)
    config.set('email', 'user@example.com')
    config.set('username', 'abc')
    errors = config.validate_all()
    assert len(errors) == 0
    
    # Test invalid port
    config.set('port', 70000)  # Out of range
    errors = config.validate_all()
    assert len(errors) == 1
    assert 'port' in errors[0]
    
    # Test invalid email
    config.set('port', 3000)  # Fix port
    config.set('email', 'invalid-email')  # Invalid email
    errors = config.validate_all()
    assert len(errors) == 1
    assert 'email' in errors[0]
    
    # Test invalid username
    config.set('email', 'valid@test.com')  # Fix email
    config.set('username', 'ab')  # Too short
    errors = config.validate_all()
    assert len(errors) == 1
    assert 'username' in errors[0]


def test_type_validation():
    """Test type hint validation."""
    config = Config()
    config.set_default('count', 0, int)
    config.set_default('price', 0.0, float)
    config.set_default('enabled', False, bool)
    config.set_default('items', [], list)
    config.set_default('metadata', {}, dict)
    config.set_default('name', '', str)
    
    # Test correct types
    config.set('count', 42)
    config.set('price', 9.99)
    config.set('enabled', True)
    config.set('items', [1, 2, 3])
    config.set('metadata', {'key': 'value'})
    config.set('name', 'test')
    errors = config.validate_all()
    assert len(errors) == 0
    
    # Test incorrect types
    config.set('count', 'not-an-int')
    config.set('price', 'not-a-float')
    config.set('enabled', 'not-a-bool')
    config.set('items', 'not-a-list')
    config.set('metadata', 'not-a-dict')
    errors = config.validate_all()
    assert len(errors) == 5  # One for each type mismatch
    
    # Check that error messages mention type mismatch
    error_text = ' '.join(errors)
    assert 'Type mismatch' in error_text
    assert 'count' in error_text
    assert 'price' in error_text
    assert 'enabled' in error_text
    assert 'items' in error_text
    assert 'metadata' in error_text


def test_get_nested():
    """Test nested configuration access."""
    config = Config()
    
    # Test getting from nested structure
    config.set('a.b.c', 'deep_value')
    config.set('a.b.x', 'shallow')
    config.set('simple', 'value')
    
    assert config.get('a.b.c') == 'deep_value'
    assert config.get('a.b') == {'c': 'deep_value', 'x': 'shallow'}
    assert config.get('a.b.x') == 'shallow'
    assert config.get('simple') == 'value'
    assert config.get('nonexistent', 'default') == 'default'
    assert config.get('a.nonexistent', 'default') == 'default'


def test_set_nested():
    """Test nested configuration setting."""
    config = Config()
    
    # Test setting nested values
    config.set('x.y.z', 'value')
    assert config.get('x.y.z') == 'value'
    assert config.get('x.y') == {'z': 'value'}
    assert config.get('x') == {'y': {'z': 'value'}}
    
    # Test overwriting nested values
    config.set('x.y.z', 'new_value')
    assert config.get('x.y.z') == 'new_value'
    
    # Test setting intermediate levels
    config.set('a.b', {'existing': 'value'})
    config.set('a.b.new_key', 'new_value')
    assert config.get('a.b') == {'existing': 'value', 'new_key': 'new_value'}


def test_to_dict():
    """Test converting configuration to dictionary."""
    config = Config()
    config.set('simple', 'value')
    config.set('nested.key', 'nested_value')
    config.set('another.nested.deep', 'deep_value')
    
    result = config.to_dict()
    expected = {
        'simple': 'value',
        'nested': {
            'key': 'nested_value'
        },
        'another': {
            'nested': {
                'deep': 'deep_value'
            }
        }
    }
    assert result == expected


if __name__ == '__main__':
    test_set_default()
    test_load_from_env()
    test_load_from_file()
    test_get_with_default()
    test_set_and_get()
    test_required_fields()
    test_custom_validators()
    test_type_validation()
    test_get_nested()
    test_set_nested()
    test_to_dict()
    print("All tests passed!")
