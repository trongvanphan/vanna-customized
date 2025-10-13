"""
myDbAssistant UI Configuration Package

This package provides flexible JSON-based configuration for the myDbAssistant application.

Usage:
    from ui.config_loader import get_vanna_config, get_database_connection_params
    from ui.config_loader import DataLoader, ConfigLoader
    
    # Get configurations
    vanna_config = get_vanna_config()
    db_params = get_database_connection_params()
    
    # Load training data
    data_loader = DataLoader()
    ddl = data_loader.load_all_ddl()
"""

from .config_loader import (
    ConfigLoader,
    DataLoader,
    get_vanna_config,
    get_database_connection_params,
    get_flask_params,
    get_initial_training_data,
    print_config_summary,
    should_auto_train,
    train_from_files,
)

__all__ = [
    'ConfigLoader',
    'DataLoader',
    'get_vanna_config',
    'get_database_connection_params',
    'get_flask_params',
    'get_initial_training_data',
    'print_config_summary',
    'should_auto_train',
    'train_from_files',
]

__version__ = '1.0.0'
