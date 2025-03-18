from mcp.server.fastmcp import FastMCP, Context
from typing import Optional
from unity_connection import get_unity_connection

def register_editor_tools(mcp: FastMCP):
    """Register all editor control tools with the MCP server."""
    
    @mcp.tool()
    def undo(ctx: Context) -> str:
        """Undo the last action performed in the Unity editor.
        
        Returns:
            str: Success message or error details
        """
        try:
            response = get_unity_connection().send_command("EDITOR_CONTROL", {
                "command": "UNDO"
            })
            return response.get("message", "Undo performed successfully")
        except Exception as e:
            return f"Error performing undo: {str(e)}"

    @mcp.tool()
    def redo(ctx: Context) -> str:
        """Redo the last undone action in the Unity editor.
        
        Returns:
            str: Success message or error details
        """
        try:
            response = get_unity_connection().send_command("EDITOR_CONTROL", {
                "command": "REDO"
            })
            return response.get("message", "Redo performed successfully")
        except Exception as e:
            return f"Error performing redo: {str(e)}"

    @mcp.tool()
    def play(ctx: Context) -> str:
        """Start the game in play mode within the Unity editor.
        
        Returns:
            str: Success message or error details
        """
        try:
            response = get_unity_connection().send_command("EDITOR_CONTROL", {
                "command": "PLAY"
            })
            return response.get("message", "Entered play mode")
        except Exception as e:
            return f"Error entering play mode: {str(e)}"

    @mcp.tool()
    def pause(ctx: Context) -> str:
        """Pause the game while in play mode.
        
        Returns:
            str: Success message or error details
        """
        try:
            response = get_unity_connection().send_command("EDITOR_CONTROL", {
                "command": "PAUSE"
            })
            return response.get("message", "Game paused")
        except Exception as e:
            return f"Error pausing game: {str(e)}"

    @mcp.tool()
    def stop(ctx: Context) -> str:
        """Stop the game and exit play mode.
        
        Returns:
            str: Success message or error details
        """
        try:
            response = get_unity_connection().send_command("EDITOR_CONTROL", {
                "command": "STOP"
            })
            return response.get("message", "Exited play mode")
        except Exception as e:
            return f"Error stopping game: {str(e)}"

    @mcp.tool()
    def build(ctx: Context, platform: str, build_path: str) -> str:
        """Build the project for a specified platform.
        
        Args:
            platform: Target platform (windows, mac, linux, android, ios, webgl)
            build_path: Path where the build should be saved
            
        Returns:
            str: Success message or error details
        """
        try:
            response = get_unity_connection().send_command("EDITOR_CONTROL", {
                "command": "BUILD",
                "params": {
                    "platform": platform,
                    "buildPath": build_path
                }
            })
            return response.get("message", "Build completed successfully")
        except Exception as e:
            return f"Error building project: {str(e)}"

    @mcp.tool()
    def execute_command(ctx: Context, command_name: str) -> str:
        """Execute a specific editor command or custom script within the Unity editor.
        
        Args:
            command_name: Name of the editor command to execute (e.g., "Edit/Preferences")
            
        Returns:
            str: Success message or error details
        """
        try:
            response = get_unity_connection().send_command("EDITOR_CONTROL", {
                "command": "EXECUTE_COMMAND",
                "params": {
                    "commandName": command_name
                }
            })
            return response.get("message", f"Executed command: {command_name}")
        except Exception as e:
            return f"Error executing command: {str(e)}" 