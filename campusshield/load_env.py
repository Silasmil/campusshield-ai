#!/usr/bin/env python
"""
Load environment variables from .env file
Supports both .env.development and .env.production
"""
import os
from pathlib import Path

def load_env_file():
    """Load environment variables from .env or .env.{environment} file"""
    
    env_type = os.environ.get('DJANGO_ENVIRONMENT', 'development')
    
    # Try environment-specific file first
    env_file = Path(__file__).resolve().parent / f'.env.{env_type}'
    if not env_file.exists():
        # Fall back to generic .env file
        env_file = Path(__file__).resolve().parent / '.env'
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                # Parse key=value
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # Only set if not already set
                    if key not in os.environ:
                        os.environ[key] = value
    
    return env_type

# Load environment on import
ENVIRONMENT = load_env_file()
