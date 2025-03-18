from mcp.server.fastmcp import FastMCP, Context
from typing import List
from unity_connection import get_unity_connection

def register_material_tools(mcp: FastMCP):
    """Register all material-related tools with the MCP server."""
    
    @mcp.tool()
    def set_material(
        ctx: Context,
        object_name: str,
        material_name: str = None,
        color: List[float] = None
    ) -> str:
        """
        Apply or create a material for a game object.
        
        Args:
            object_name: Target game object.
            material_name: Optional material name.
            color: Optional [R, G, B] values (0.0-1.0).
        """
        try:
            unity = get_unity_connection()
            params = {"object_name": object_name}
            if material_name:
                params["material_name"] = material_name
            if color:
                params["color"] = color
            result = unity.send_command("SET_MATERIAL", params)
            return f"Applied material to {object_name}: {result.get('material_name', 'unknown')}"
        except Exception as e:
            return f"Error setting material: {str(e)}" 