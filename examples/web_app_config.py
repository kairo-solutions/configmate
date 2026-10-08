"""
Example: Using ConfigMate in a web application
"""

from configmate.config import config
import os


def setup_web_app_config():
    """Configure a web application using ConfigMate."""
    
    # Set default values
    config.set_default('debug', False, bool)
    config.set_default('host', '127.0.0.1', str)
    config.set_default('port', 8000, int)
    config.set_default('log_level', 'INFO', str)
    
    # Database configuration
    config.set_default('database.host', 'localhost', str)
    config.set_default('database.port', 5432, int)
    config.set_default('database.name', 'myapp', str)
    config.set_default('database.user', '', str)
    config.set_default('database.password', '', str)
    config.set_default('database.pool_size', 5, int)
    
    # API configuration
    config.set_default('api.rate_limit', 100, int)
    config.set_default('api.timeout', 30, int)
    config.set_default('api.retry_attempts', 3, int)
    
    # Feature flags
    config.set_default('features.new_ui', False, bool)
    config.set_default('features.api_v2', True, bool)
    config.set_default('features.cache_enabled', True, bool)
    
    # Mark required fields
    config.require('database.user')
    config.require('database.password')
    
    # Add validation
    config.validate('port', lambda x: 1 <= x <= 65535)
    config.validate('database.pool_size', lambda x: 1 <= x <= 20)
    config.validate('api.rate_limit', lambda x: x >= 1)
    config.validate('log_level', lambda x: x in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    
    # Load configuration from multiple sources
    config.load_from_env(prefix='WEBAPP_')  # WEBAPP_DEBUG, WEBAPP_DATABASE__USER, etc.
    config.load_from_file('config/webapp.json')  # Optional config file
    
    # Validate everything
    errors = config.validate_all()
    if errors:
        raise RuntimeError(f"Configuration errors: {', '.join(errors)}")
    
    return config


def get_database_url():
    """Construct database URL from configuration."""
    db = config
    return (
        f"postgresql://{db.get('database.user')}:{db.get('database.password')}@"
        f"{db.get('database.host')}:{db.get('database.port')}/"
        f"{db.get('database.name')}"
    )


def is_feature_enabled(feature_name):
    """Check if a feature is enabled."""
    return config.get(f'features.{feature_name}', False)


if __name__ == '__main__':
    # Example usage
    try:
        cfg = setup_web_app_config()
        print("✅ Configuration loaded successfully!")
        print(f"🌐 Server: {cfg.get('host')}:{cfg.get('port')}")
        print(f"🔗 Database: {get_database_url()}")
        print(f"📊 Log level: {cfg.get('log_level')}")
        print(f"⚡ Features - New UI: {is_feature_enabled('new_ui')}, "
              f"API v2: {is_feature_enabled('api_v2')}")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        exit(1)
