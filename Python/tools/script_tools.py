from mcp.server.fastmcp import FastMCP, Context
from typing import List
from unity_connection import get_unity_connection

def register_script_tools(mcp: FastMCP):
    """Register all script-related tools with the MCP server."""
    
    @mcp.tool()
    def view_script(ctx: Context, script_path: str) -> str:
        """View the contents of a Unity script file.
        
        Args:
            ctx: The MCP context
            script_path: Path to the script file relative to the Assets folder
            
        Returns:
            str: The contents of the script file or error message
        """
        try:
            # Send command to Unity to read the script file
            response = get_unity_connection().send_command("VIEW_SCRIPT", {
                "script_path": script_path
            })
            return response.get("content", "Script not found")
        except Exception as e:
            return f"Error viewing script: {str(e)}"

    @mcp.tool()
    def create_script(
        ctx: Context,
        script_name: str,
        script_type: str = "MonoBehaviour",
        namespace: str = None,
        template: str = None
    ) -> str:
        """Create a new Unity script file.
        
        Args:
            ctx: The MCP context
            script_name: Name of the script (without .cs extension)
            script_type: Type of script (e.g., MonoBehaviour, ScriptableObject)
            namespace: Optional namespace for the script
            template: Optional custom template to use
            
        Returns:
            str: Success message or error details
        """
        try:
            # Send command to Unity to create the script
            response = get_unity_connection().send_command("CREATE_SCRIPT", {
                "script_name": script_name,
                "script_type": script_type,
                "namespace": namespace,
                "template": template
            })
            return response.get("message", "Script created successfully")
        except Exception as e:
            return f"Error creating script: {str(e)}"

    @mcp.tool()
    def update_script(
        ctx: Context,
        script_path: str,
        content: str
    ) -> str:
        """Update the contents of an existing Unity script.
        
        Args:
            ctx: The MCP context
            script_path: Path to the script file relative to the Assets folder
            content: New content for the script
            
        Returns:
            str: Success message or error details
        """
        try:
            # Send command to Unity to update the script
            response = get_unity_connection().send_command("UPDATE_SCRIPT", {
                "script_path": script_path,
                "content": content
            })
            return response.get("message", "Script updated successfully")
        except Exception as e:
            return f"Error updating script: {str(e)}"

    @mcp.tool()
    def list_scripts(ctx: Context, folder_path: str = "Assets") -> str:
        """List all script files in a specified folder.
        
        Args:
            ctx: The MCP context
            folder_path: Path to the folder to search (default: Assets)
            
        Returns:
            str: List of script files or error message
        """
        try:
            # Send command to Unity to list scripts
            response = get_unity_connection().send_command("LIST_SCRIPTS", {
                "folder_path": folder_path
            })
            scripts = response.get("scripts", [])
            if not scripts:
                return "No scripts found in the specified folder"
            return "\n".join(scripts)
        except Exception as e:
            return f"Error listing scripts: {str(e)}"

    @mcp.tool()
    def attach_script(
        ctx: Context,
        object_name: str,
        script_name: str
    ) -> str:
        """Attach a script component to a GameObject.
        
        Args:
            ctx: The MCP context
            object_name: Name of the target GameObject in the scene
            script_name: Name of the script to attach (with or without .cs extension)
            
        Returns:
            str: Success message or error details
        """
        try:
            # Send command to Unity to attach the script
            response = get_unity_connection().send_command("ATTACH_SCRIPT", {
                "object_name": object_name,
                "script_name": script_name
            })
            return response.get("message", "Script attached successfully")
        except Exception as e:
            return f"Error attaching script: {str(e)}" 