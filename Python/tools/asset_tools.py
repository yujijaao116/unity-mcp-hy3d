from typing import Optional
from mcp.server.fastmcp import FastMCP, Context
from unity_connection import get_unity_connection

def register_asset_tools(mcp: FastMCP):
    """Register all asset management tools with the MCP server."""
    
    @mcp.tool()
    def import_asset(
        ctx: Context,
        source_path: str,
        target_path: str
    ) -> str:
        """Import an asset (e.g., 3D model, texture) into the Unity project.

        Args:
            ctx: The MCP context
            source_path: Path to the source file on disk
            target_path: Path where the asset should be imported in the Unity project (relative to Assets folder)

        Returns:
            str: Success message or error details
        """
        try:
            # Parameter validation
            if not source_path or not isinstance(source_path, str):
                return f"Error importing asset: source_path must be a valid string"
            
            if not target_path or not isinstance(target_path, str):
                return f"Error importing asset: target_path must be a valid string"
                
            response = get_unity_connection().send_command("IMPORT_ASSET", {
                "source_path": source_path,
                "target_path": target_path
            })
            
            if not response.get("success", False):
                return f"Error importing asset: {response.get('error', 'Unknown error')} (Source: {source_path}, Target: {target_path})"
                
            return response.get("message", "Asset imported successfully")
        except Exception as e:
            return f"Error importing asset: {str(e)} (Source: {source_path}, Target: {target_path})"

    @mcp.tool()
    def instantiate_prefab(
        ctx: Context,
        prefab_path: str,
        position_x: float = 0.0,
        position_y: float = 0.0,
        position_z: float = 0.0,
        rotation_x: float = 0.0,
        rotation_y: float = 0.0,
        rotation_z: float = 0.0
    ) -> str:
        """Instantiate a prefab into the current scene at a specified location.

        Args:
            ctx: The MCP context
            prefab_path: Path to the prefab asset (relative to Assets folder)
            position_x: X position in world space (default: 0.0)
            position_y: Y position in world space (default: 0.0)
            position_z: Z position in world space (default: 0.0)
            rotation_x: X rotation in degrees (default: 0.0)
            rotation_y: Y rotation in degrees (default: 0.0)
            rotation_z: Z rotation in degrees (default: 0.0)

        Returns:
            str: Success message or error details
        """
        try:
            # Parameter validation
            if not prefab_path or not isinstance(prefab_path, str):
                return f"Error instantiating prefab: prefab_path must be a valid string"
                
            # Validate numeric parameters
            position_params = {
                "position_x": position_x,
                "position_y": position_y,
                "position_z": position_z,
                "rotation_x": rotation_x,
                "rotation_y": rotation_y,
                "rotation_z": rotation_z
            }
            
            for param_name, param_value in position_params.items():
                if not isinstance(param_value, (int, float)):
                    return f"Error instantiating prefab: {param_name} must be a number"
            
            response = get_unity_connection().send_command("INSTANTIATE_PREFAB", {
                "prefab_path": prefab_path,
                "position_x": position_x,
                "position_y": position_y,
                "position_z": position_z,
                "rotation_x": rotation_x,
                "rotation_y": rotation_y,
                "rotation_z": rotation_z
            })
            
            if not response.get("success", False):
                return f"Error instantiating prefab: {response.get('error', 'Unknown error')} (Path: {prefab_path})"
                
            return f"Prefab instantiated successfully as '{response.get('instance_name', 'unknown')}'"
        except Exception as e:
            return f"Error instantiating prefab: {str(e)} (Path: {prefab_path})"

    @mcp.tool()
    def create_prefab(
        ctx: Context,
        object_name: str,
        prefab_path: str
    ) -> str:
        """Create a new prefab asset from a GameObject in the scene.

        Args:
            ctx: The MCP context
            object_name: Name of the GameObject in the scene to create prefab from
            prefab_path: Path where the prefab should be saved (relative to Assets folder)

        Returns:
            str: Success message or error details
        """
        try:
            # Parameter validation
            if not object_name or not isinstance(object_name, str):
                return f"Error creating prefab: object_name must be a valid string"
                
            if not prefab_path or not isinstance(prefab_path, str):
                return f"Error creating prefab: prefab_path must be a valid string"
                
            # Verify prefab path has proper extension
            if not prefab_path.lower().endswith('.prefab'):
                prefab_path = f"{prefab_path}.prefab"
            
            response = get_unity_connection().send_command("CREATE_PREFAB", {
                "object_name": object_name,
                "prefab_path": prefab_path
            })
            
            if not response.get("success", False):
                return f"Error creating prefab: {response.get('error', 'Unknown error')} (Object: {object_name}, Path: {prefab_path})"
                
            return f"Prefab created successfully at {response.get('path', prefab_path)}"
        except Exception as e:
            return f"Error creating prefab: {str(e)} (Object: {object_name}, Path: {prefab_path})"

    @mcp.tool()
    def apply_prefab(
        ctx: Context,
        object_name: str
    ) -> str:
        """Apply changes made to a prefab instance back to the original prefab asset.

        Args:
            ctx: The MCP context
            object_name: Name of the prefab instance in the scene

        Returns:
            str: Success message or error details
        """
        try:
            response = get_unity_connection().send_command("APPLY_PREFAB", {
                "object_name": object_name
            })
            return response.get("message", "Prefab changes applied successfully")
        except Exception as e:
            return f"Error applying prefab changes: {str(e)}" 