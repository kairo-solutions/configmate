"""
Command-line interface for ConfigMate
"""

import argparse
import sys
import json
from pathlib import Path
from ..config import config


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ConfigMate - Configuration management utility"
    )
    parser.add_argument(
        '--version', action='version', version='ConfigMate 0.1.0'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Set command
    set_parser = subparsers.add_parser('set', help='Set a configuration value')
    set_parser.add_argument('key', help='Configuration key')
    set_parser.add_argument('value', help='Configuration value')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get a configuration value')
    get_parser.add_argument('key', help='Configuration key')
    get_parser.add_argument(
        '--default', help='Default value if key not found'
    )
    
    # Load command
    load_parser = subparsers.add_parser('load', help='Load configuration from file')
    load_parser.add_argument('file', help='Configuration file to load')
    
    # Env command
    env_parser = subparsers.add_parser('env', help='Load configuration from environment')
    env_parser.add_argument(
        '--prefix', default='', help='Environment variable prefix'
    )
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all configuration values')
    
    args = parser.parse_args()
    
    if args.command == 'set':
        # Try to convert value to appropriate type
        try:
            # Try JSON first (for objects, arrays, booleans, numbers)
            value = json.loads(args.value)
        except json.JSONDecodeError:
            # If not JSON, treat as string
            value = args.value
        
        config.set(args.key, value)
        print(f"Set {args.key} = {value}")
    
    elif args.command == 'get':
        value = config.get(args.key, args.default)
        if value is None:
            print(f"Key '{args.key}' not found", file=sys.stderr)
            sys.exit(1)
        else:
            if isinstance(value, (dict, list)):
                print(json.dumps(value, indent=2))
            else:
                print(value)
    
    elif args.command == 'load':
        try:
            config.load_from_file(args.file)
            print(f"Loaded configuration from {args.file}")
        except Exception as e:
            print(f"Error loading configuration: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'env':
        config.load_from_env(prefix=args.prefix)
        print(f"Loaded configuration from environment with prefix '{args.prefix}'")
    
    elif args.command == 'list':
        # Show all configuration values
        for key in sorted(config._config.keys()):
            value = config._config[key]
            if isinstance(value, (dict, list)):
                print(f"{key} = {json.dumps(value)}")
            else:
                print(f"{key} = {value}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
