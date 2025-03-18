"""
Configuration settings for the Unity MCP Server.
This file contains all configurable parameters for the server.
"""

from dataclasses import dataclass
from typing import Dict, Any
import json
import os

@dataclass
class ServerConfig:
    """Main configuration class for the MCP server."""
    
    # Network settings
    unity_host: str
    unity_port: int
    mcp_port: int
    
    # Connection settings
    connection_timeout: float
    buffer_size: int
    
    # Logging settings
    log_level: str
    log_format: str
    
    # Server settings
    max_retries: int
    retry_delay: float
    
    @classmethod
    def from_file(cls, config_path: str = None) -> "ServerConfig":
        """Load configuration from a JSON file."""
        if config_path is None:
            # Get the directory where this file is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one directory to find config.json
            config_path = os.path.join(os.path.dirname(current_dir), "config.json")
            
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at {config_path}. Please ensure config.json exists.")
            
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
            return cls(**config_dict)
    
    def to_file(self, config_path: str = None) -> None:
        """Save configuration to a JSON file."""
        if config_path is None:
            # Get the directory where this file is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one directory to find config.json
            config_path = os.path.join(os.path.dirname(current_dir), "config.json")
            
        config_dict = {
            "unity_host": self.unity_host,
            "unity_port": self.unity_port,
            "mcp_port": self.mcp_port,
            "connection_timeout": self.connection_timeout,
            "buffer_size": self.buffer_size,
            "log_level": self.log_level,
            "log_format": self.log_format,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay
        }
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=4)

# Create a global config instance
try:
    config = ServerConfig.from_file()
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Please ensure config.json exists in the Assets/MCPServer directory")
    raise 