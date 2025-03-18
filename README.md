# Unity Model Context Protocol (MCP) Server

A bridge between Python and Unity that allows for programmatic control of the Unity Editor through Python scripts.

## Overview

The Unity MCP Server provides a bidirectional communication channel between Python and the Unity Editor, enabling:

- Creation and manipulation of Unity assets
- Scene management and object manipulation
- Material and script editing
- Editor control and automation

This system is designed to make Unity Editor operations programmable through Python, allowing for more complex automation workflows and integrations.

## Structure

- **Editor/**: C# implementation of Unity-side command handlers
  - **Commands/**: Command handlers organized by functionality
  - **Models/**: Data models and contract definitions
  - **Helpers/**: Utility classes for common operations
  - **MCPServerWindow.cs**: Unity Editor window for controlling the MCP Server
  - **UnityMCPBridge.cs**: Core communication bridge implementation

- **Python/**: Python server implementation
  - **tools/**: Python tool implementations that map to Unity commands
  - **server.py**: FastAPI server implementation
  - **unity_connection.py**: Communication layer for Unity connection

## Installation

1. Import this package into your Unity project
2. Install Python requirements:
   ```bash
   cd Assets/MCPServer/Python
   pip install -e .
   ```

## Usage

1. Set up MCP integration in Unity:
   - Open Window > Unity MCP
   - Click the configuration button to set up integration with MCP clients like Claude Desktop or Cursor

2. The Unity Bridge will start automatically when the Unity Editor launches, and the Python server will be started by the MCP client when needed.

3. Use Python tools to control Unity through the MCP client:
   ```python
   # Example: Create a new cube in the scene
   create_primitive(primitive_type="Cube", position=[0, 0, 0])
   
   # Example: Change material color
   set_material_color(material_name="MyMaterial", color=[1, 0, 0, 1])
   ```

## Adding New Tools

See [HOW_TO_ADD_A_TOOL.md](HOW_TO_ADD_A_TOOL.md) for detailed instructions on extending the MCP Server with your own tools.

## Best Practices

- Always validate parameters on both Python and C# sides
- Use try-catch blocks for error handling in both environments
- Follow the established naming conventions (UPPER_SNAKE_CASE for commands, snake_case for Python tools)
- Group related functionality in appropriate tool modules and command handlers

## Testing

Run Python tests with:
```bash
python -m unittest discover Assets/MCPServer/Python/tests
```

## Troubleshooting

- Check Unity Console for C# errors
- Verify your MCP client (Claude Desktop, Cursor) is properly configured
- Check the MCP integration status in Window > Unity MCP
- Check network connectivity between Unity and the MCP client
- Ensure commands are properly registered in CommandRegistry.cs
- Verify Python tools are properly imported and registered