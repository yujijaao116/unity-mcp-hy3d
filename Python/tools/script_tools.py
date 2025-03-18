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
        template: str = None,
        overwrite: bool = False
    ) -> str:
        """Create a new Unity script file.
        
        Args:
            ctx: The MCP context
            script_name: Name of the script (without .cs extension)
            script_type: Type of script (e.g., MonoBehaviour, ScriptableObject)
            namespace: Optional namespace for the script
            template: Optional custom template to use
            overwrite: Whether to overwrite if script already exists (default: False)
            
        Returns:
            str: Success message or error details
        """
        try:
            # First check if a script with this name already exists
            unity = get_unity_connection()
            script_path = f"Assets/Scripts/{script_name}.cs"
            
            # Try to view the script to check if it exists
            existing_script_response = unity.send_command("VIEW_SCRIPT", {
                "script_path": script_path
            })
            
            # If the script exists and overwrite is False, return a message
            if "content" in existing_script_response and not overwrite:
                return f"Script '{script_name}.cs' already exists. Use overwrite=True to replace it."
            
            # Send command to Unity to create the script
            response = unity.send_command("CREATE_SCRIPT", {
                "script_name": script_name,
                "script_type": script_type,
                "namespace": namespace,
                "template": template,
                "overwrite": overwrite
            })
            return response.get("message", "Script created successfully")
        except Exception as e:
            return f"Error creating script: {str(e)}"

    @mcp.tool()
    def update_script(
        ctx: Context,
        script_path: str,
        content: str,
        create_if_missing: bool = False,
        create_folder_if_missing: bool = False
    ) -> str:
        """Update the contents of an existing Unity script.
        
        Args:
            ctx: The MCP context
            script_path: Path to the script file relative to the Assets folder
            content: New content for the script
            create_if_missing: Whether to create the script if it doesn't exist (default: False)
            create_folder_if_missing: Whether to create the parent directory if it doesn't exist (default: False)
            
        Returns:
            str: Success message or error details
        """
        try:
            unity = get_unity_connection()
            
            # Parse script path (for potential creation)
            script_name = script_path.split("/")[-1].replace(".cs", "")
            script_folder = "/".join(script_path.split("/")[:-1])
            
            if create_if_missing:
                # When create_if_missing is true, we'll just try to update directly,
                # and let Unity handle the creation if needed
                params = {
                    "script_path": script_path,
                    "content": content,
                    "create_if_missing": True
                }
                
                # Add folder creation flag if requested
                if create_folder_if_missing:
                    params["create_folder_if_missing"] = True
                    
                # Send command to Unity to update/create the script
                response = unity.send_command("UPDATE_SCRIPT", params)
                return response.get("message", "Script updated successfully")
            else:
                # Standard update without creation flags
                response = unity.send_command("UPDATE_SCRIPT", {
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
        script_name: str,
        script_path: str = None
    ) -> str:
        """Attach a script component to a GameObject.
        
        Args:
            ctx: The MCP context
            object_name: Name of the target GameObject in the scene
            script_name: Name of the script to attach (with or without .cs extension)
            script_path: Optional full path to the script (if not in the default Scripts folder)
            
        Returns:
            str: Success message or error details
        """
        try:
            unity = get_unity_connection()
            
            # Check if the object exists
            object_response = unity.send_command("FIND_OBJECTS_BY_NAME", {
                "name": object_name
            })
            
            objects = object_response.get("objects", [])
            if not objects:
                return f"GameObject '{object_name}' not found in the scene."
            
            # Ensure script_name has .cs extension
            if not script_name.lower().endswith(".cs"):
                script_name = f"{script_name}.cs"
            
            # Determine the full script path
            if script_path is None:
                # Use default Scripts folder if no path provided
                script_path = f"Assets/Scripts/{script_name}"
            elif not script_path.endswith(script_name):
                # If path is just a directory, append the script name
                if script_path.endswith("/"):
                    script_path = f"{script_path}{script_name}"
                else:
                    script_path = f"{script_path}/{script_name}"
            
            # Check if the script exists by trying to view it
            existing_script_response = unity.send_command("VIEW_SCRIPT", {
                "script_path": script_path
            })
            
            if "content" not in existing_script_response:
                # If not found at the specific path, try to search for it in the project
                script_found = False
                try:
                    # Search in the entire Assets folder
                    script_assets = unity.send_command("LIST_SCRIPTS", {
                        "folder_path": "Assets"
                    }).get("scripts", [])
                    
                    # Look for matching script name in any folder
                    matching_scripts = [path for path in script_assets if path.endswith(f"/{script_name}") or path == script_name]
                    
                    if matching_scripts:
                        script_path = matching_scripts[0]
                        script_found = True
                        if len(matching_scripts) > 1:
                            return f"Multiple scripts named '{script_name}' found in the project. Please specify script_path parameter."
                except:
                    pass
                
                if not script_found:
                    return f"Script '{script_name}' not found in the project."
            
            # Check if the script is already attached
            object_props = unity.send_command("GET_OBJECT_PROPERTIES", {
                "name": object_name
            })
            
            # Extract script name without .cs and without path
            script_class_name = script_name.replace(".cs", "")
            
            # Check if component is already attached
            components = object_props.get("components", [])
            for component in components:
                if component.get("type") == script_class_name:
                    return f"Script '{script_class_name}' is already attached to '{object_name}'."
            
            # Send command to Unity to attach the script
            response = unity.send_command("ATTACH_SCRIPT", {
                "object_name": object_name,
                "script_name": script_name,
                "script_path": script_path
            })
            return response.get("message", "Script attached successfully")
        except Exception as e:
            return f"Error attaching script: {str(e)}" 