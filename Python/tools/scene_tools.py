from mcp.server.fastmcp import FastMCP, Context
from typing import List, Dict, Any, Optional
import json
from unity_connection import get_unity_connection

def register_scene_tools(mcp: FastMCP):
    """Register all scene-related tools with the MCP server."""
    
    @mcp.tool()
    def get_scene_info(ctx: Context) -> str:
        """Retrieve detailed info about the current Unity scene."""
        try:
            unity = get_unity_connection()
            result = unity.send_command("GET_SCENE_INFO")
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting scene info: {str(e)}"

    @mcp.tool()
    def open_scene(ctx: Context, scene_path: str) -> str:
        """Open a specified scene in the Unity editor.
        
        Args:
            scene_path: Full path to the scene file (e.g., "Assets/Scenes/MyScene.unity")
            
        Returns:
            str: Success message or error details
        """
        try:
            unity = get_unity_connection()
            result = unity.send_command("OPEN_SCENE", {"scene_path": scene_path})
            return result.get("message", "Scene opened successfully")
        except Exception as e:
            return f"Error opening scene: {str(e)}"

    @mcp.tool()
    def save_scene(ctx: Context) -> str:
        """Save the current scene to its file.
        
        Returns:
            str: Success message or error details
        """
        try:
            unity = get_unity_connection()
            result = unity.send_command("SAVE_SCENE")
            return result.get("message", "Scene saved successfully")
        except Exception as e:
            return f"Error saving scene: {str(e)}"

    @mcp.tool()
    def new_scene(ctx: Context, scene_path: str) -> str:
        """Create a new empty scene in the Unity editor.
        
        Args:
            scene_path: Full path where the new scene should be saved (e.g., "Assets/Scenes/NewScene.unity")
            
        Returns:
            str: Success message or error details
        """
        try:
            unity = get_unity_connection()
            # Create new scene
            result = unity.send_command("NEW_SCENE", {"scene_path": scene_path})
            
            # Save the scene to ensure it's properly created
            unity.send_command("SAVE_SCENE")
            
            # Get scene info to verify it's loaded
            scene_info = unity.send_command("GET_SCENE_INFO")
            
            return result.get("message", "New scene created successfully")
        except Exception as e:
            return f"Error creating new scene: {str(e)}"

    @mcp.tool()
    def change_scene(ctx: Context, scene_path: str, save_current: bool = False) -> str:
        """Change to a different scene, optionally saving the current one.
        
        Args:
            scene_path: Full path to the target scene file (e.g., "Assets/Scenes/TargetScene.unity")
            save_current: Whether to save the current scene before changing (default: False)
            
        Returns:
            str: Success message or error details
        """
        try:
            unity = get_unity_connection()
            result = unity.send_command("CHANGE_SCENE", {
                "scene_path": scene_path,
                "save_current": save_current
            })
            return result.get("message", "Scene changed successfully")
        except Exception as e:
            return f"Error changing scene: {str(e)}"

    @mcp.tool()
    def get_object_info(ctx: Context, object_name: str) -> str:
        """
        Get info about a specific game object.
        
        Args:
            object_name: Name of the game object.
        """
        try:
            unity = get_unity_connection()
            result = unity.send_command("GET_OBJECT_INFO", {"name": object_name})
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error getting object info: {str(e)}"

    @mcp.tool()
    def create_object(
        ctx: Context,
        type: str = "CUBE",
        name: str = None,
        location: List[float] = None,
        rotation: List[float] = None,
        scale: List[float] = None
    ) -> str:
        """
        Create a game object in the Unity scene.
        
        Args:
            type: Object type (CUBE, SPHERE, CYLINDER, CAPSULE, PLANE, EMPTY, CAMERA, LIGHT).
            name: Optional name for the game object.
            location: [x, y, z] position (defaults to [0, 0, 0]).
            rotation: [x, y, z] rotation in degrees (defaults to [0, 0, 0]).
            scale: [x, y, z] scale factors (defaults to [1, 1, 1]).
        
        Returns:
            Confirmation message with the created object's name.
        """
        try:
            unity = get_unity_connection()
            params = {
                "type": type.upper(),
                "location": location or [0, 0, 0],
                "rotation": rotation or [0, 0, 0],
                "scale": scale or [1, 1, 1]
            }
            if name:
                params["name"] = name
            result = unity.send_command("CREATE_OBJECT", params)
            return f"Created {type} game object: {result['name']}"
        except Exception as e:
            return f"Error creating game object: {str(e)}"

    @mcp.tool()
    def modify_object(
        ctx: Context,
        name: str,
        location: Optional[List[float]] = None,
        rotation: Optional[List[float]] = None,
        scale: Optional[List[float]] = None,
        visible: Optional[bool] = None,
        set_parent: Optional[str] = None,
        add_component: Optional[str] = None,
        remove_component: Optional[str] = None,
        set_property: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Modify a game object's properties and components.
        
        Args:
            name: Name of the game object to modify.
            location: Optional [x, y, z] position.
            rotation: Optional [x, y, z] rotation in degrees.
            scale: Optional [x, y, z] scale factors.
            visible: Optional visibility toggle.
            set_parent: Optional name of the parent object to set.
            add_component: Optional name of the component type to add (e.g., "Rigidbody", "BoxCollider").
            remove_component: Optional name of the component type to remove.
            set_property: Optional dict with keys:
                - component: Name of the component type
                - property: Name of the property to set
                - value: Value to set the property to
        
        Returns:
            str: Success message or error details
        """
        try:
            unity = get_unity_connection()
            params = {"name": name}
            
            # Add basic transform properties
            if location is not None:
                params["location"] = location
            if rotation is not None:
                params["rotation"] = rotation
            if scale is not None:
                params["scale"] = scale
            if visible is not None:
                params["visible"] = visible
                
            # Add parent setting
            if set_parent is not None:
                params["set_parent"] = set_parent
                
            # Add component operations
            if add_component is not None:
                params["add_component"] = add_component
            if remove_component is not None:
                params["remove_component"] = remove_component
                
            # Add property setting
            if set_property is not None:
                params["set_property"] = set_property
                
            result = unity.send_command("MODIFY_OBJECT", params)
            return f"Modified game object: {result['name']}"
        except Exception as e:
            return f"Error modifying game object: {str(e)}"

    @mcp.tool()
    def delete_object(ctx: Context, name: str) -> str:
        """
        Remove a game object from the scene.
        
        Args:
            name: Name of the game object to delete.
        """
        try:
            unity = get_unity_connection()
            result = unity.send_command("DELETE_OBJECT", {"name": name})
            return f"Deleted game object: {name}"
        except Exception as e:
            return f"Error deleting game object: {str(e)}" 