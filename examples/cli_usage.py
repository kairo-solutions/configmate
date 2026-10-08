"""
Example: Using ConfigMate CLI in scripts
"""

import subprocess
import json
import tempfile
import os
from pathlib import Path


def demo_cli_usage():
    """Demonstrate various CLI usage patterns."""
    
    # Set some environment variables for the demo
    os.environ['APP_DEBUG'] = 'true'
    os.environ['APP_PORT'] = '3000'
    os.environ['APP_NAME'] = 'demo-app'
    
    print("=== ConfigMate CLI Usage Demo ===\n")
    
    # 1. Show help
    print("1. Help command:")
    result = subprocess.run(['python', '-m', 'configmate.cli', '--help'], 
                          capture_output=True, text=True)
    print(result.stdout)
    
    # 2. Load from environment
    print("2. Loading from environment:")
    subprocess.run(['python', '-m', 'configmate.cli', 'env', '--prefix', 'APP_'])
    
    # 3. List current configuration
    print("\n3. Current configuration:")
    subprocess.run(['python', '-m', 'configmate.cli', 'list'])
    
    # 4. Get specific values
    print("\n4. Getting specific values:")
    subprocess.run(['python', '-m', 'configmate.cli', 'get', 'debug'])
    subprocess.run(['python', '-m', 'configmate.cli', 'get', 'port'])
    subprocess.run(['python', '-m', 'configmate.cli', 'get', 'name'])
    
    # 5. Set a value via CLI
    print("\n5. Setting a value:")
    subprocess.run(['python', '-m', 'configmate.cli', 'set', 'feature.flag', 'true'])
    subprocess.run(['python', '-m', 'configmate.cli', 'get', 'feature.flag'])
    
    # 6. Load from file
    print("\n6. Loading from JSON file:")
    config_data = {
        "database": {
            "host": "localhost",
            "port": 5432
        },
        "logging": {
            "level": "DEBUG",
            "format": "json"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        config_file = f.name
    
    try:
        subprocess.run(['python', '-m', 'configmate.cli', 'load', config_file])
        print("After loading file:")
        subprocess.run(['python', '-m', 'configmate.cli', 'list'])
    finally:
        os.unlink(config_file)
    
    print("\n=== Demo Complete ===")


if __name__ == '__main__':
    demo_cli_usage()
