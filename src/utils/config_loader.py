"""
Configuration loading and validation utilities
"""

import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Validate required keys
    validate_config(config)
    
    return config


def validate_config(config: Dict) -> None:
    """
    Validate configuration has required fields
    
    Args:
        config: Configuration dictionary
        
    Raises:
        ValueError: If configuration is invalid
    """
    required_keys = ['system', 'hvsae', 'training', 'cse_kg']
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    
    # Validate system config
    if 'device' not in config['system']:
        config['system']['device'] = 'cpu'  # Default
    
    print("✓ Configuration validated")


def get_device(config: Dict) -> str:
    """Get device from config"""
    return config['system']['device']




















