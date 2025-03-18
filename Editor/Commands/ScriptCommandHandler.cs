using UnityEngine;
using UnityEditor;
using System.IO;
using System.Text;
using System.Linq;
using Newtonsoft.Json.Linq;
using MCPServer.Editor.Helpers;

namespace MCPServer.Editor.Commands
{
    /// <summary>
    /// Handles script-related commands for Unity
    /// </summary>
    public static class ScriptCommandHandler
    {
        /// <summary>
        /// Views the contents of a Unity script file
        /// </summary>
        public static object ViewScript(JObject @params)
        {
            string scriptPath = (string)@params["script_path"] ?? throw new System.Exception("Parameter 'script_path' is required.");
            string fullPath = Path.Combine(Application.dataPath, scriptPath);

            if (!File.Exists(fullPath))
                throw new System.Exception($"Script file not found: {scriptPath}");

            return new { content = File.ReadAllText(fullPath) };
        }

        /// <summary>
        /// Ensures the Scripts folder exists in the project
        /// </summary>
        private static void EnsureScriptsFolderExists()
        {
            string scriptsFolderPath = Path.Combine(Application.dataPath, "Scripts");
            if (!Directory.Exists(scriptsFolderPath))
            {
                Directory.CreateDirectory(scriptsFolderPath);
                AssetDatabase.Refresh();
            }
        }

        /// <summary>
        /// Creates a new Unity script file in the Scripts folder
        /// </summary>
        public static object CreateScript(JObject @params)
        {
            string scriptName = (string)@params["script_name"] ?? throw new System.Exception("Parameter 'script_name' is required.");
            string scriptType = (string)@params["script_type"] ?? "MonoBehaviour";
            string namespaceName = (string)@params["namespace"];
            string template = (string)@params["template"];

            // Ensure script name ends with .cs
            if (!scriptName.EndsWith(".cs"))
                scriptName += ".cs";

            // Ensure Scripts folder exists
            EnsureScriptsFolderExists();

            // Create namespace-based folder structure if namespace is specified
            string scriptPath = "Scripts";
            if (!string.IsNullOrEmpty(namespaceName))
            {
                scriptPath = Path.Combine(scriptPath, namespaceName.Replace('.', '/'));
                string namespaceFolderPath = Path.Combine(Application.dataPath, scriptPath);
                if (!Directory.Exists(namespaceFolderPath))
                {
                    Directory.CreateDirectory(namespaceFolderPath);
                    AssetDatabase.Refresh();
                }
            }

            // Create the script content
            StringBuilder content = new StringBuilder();

            // Add namespace if specified
            if (!string.IsNullOrEmpty(namespaceName))
            {
                content.AppendLine($"namespace {namespaceName}");
                content.AppendLine("{");
            }

            // Add class definition
            content.AppendLine($"    public class {Path.GetFileNameWithoutExtension(scriptName)} : {scriptType}");
            content.AppendLine("    {");

            // Add default Unity methods based on script type
            if (scriptType == "MonoBehaviour")
            {
                content.AppendLine("        private void Start()");
                content.AppendLine("        {");
                content.AppendLine("            // Initialize your component here");
                content.AppendLine("        }");
                content.AppendLine();
                content.AppendLine("        private void Update()");
                content.AppendLine("        {");
                content.AppendLine("            // Update your component here");
                content.AppendLine("        }");
            }
            else if (scriptType == "ScriptableObject")
            {
                content.AppendLine("        private void OnEnable()");
                content.AppendLine("        {");
                content.AppendLine("            // Initialize your ScriptableObject here");
                content.AppendLine("        }");
            }

            // Close class
            content.AppendLine("    }");

            // Close namespace if specified
            if (!string.IsNullOrEmpty(namespaceName))
            {
                content.AppendLine("}");
            }

            // Create the script file in the Scripts folder
            string fullPath = Path.Combine(Application.dataPath, scriptPath, scriptName);
            File.WriteAllText(fullPath, content.ToString());

            // Refresh the AssetDatabase
            AssetDatabase.Refresh();

            return new { message = $"Created script: {Path.Combine(scriptPath, scriptName)}" };
        }

        /// <summary>
        /// Updates the contents of an existing Unity script
        /// </summary>
        public static object UpdateScript(JObject @params)
        {
            string scriptPath = (string)@params["script_path"] ?? throw new System.Exception("Parameter 'script_path' is required.");
            string content = (string)@params["content"] ?? throw new System.Exception("Parameter 'content' is required.");

            string fullPath = Path.Combine(Application.dataPath, scriptPath);

            if (!File.Exists(fullPath))
                throw new System.Exception($"Script file not found: {scriptPath}");

            // Write new content
            File.WriteAllText(fullPath, content);

            // Refresh the AssetDatabase
            AssetDatabase.Refresh();

            return new { message = $"Updated script: {scriptPath}" };
        }

        /// <summary>
        /// Lists all script files in a specified folder
        /// </summary>
        public static object ListScripts(JObject @params)
        {
            string folderPath = (string)@params["folder_path"] ?? "Assets";
            string fullPath = Path.Combine(Application.dataPath, folderPath);

            if (!Directory.Exists(fullPath))
                throw new System.Exception($"Folder not found: {folderPath}");

            string[] scripts = Directory.GetFiles(fullPath, "*.cs", SearchOption.AllDirectories)
                .Select(path => path.Replace(Application.dataPath, "Assets"))
                .ToArray();

            return new { scripts };
        }

        /// <summary>
        /// Attaches a script component to a GameObject
        /// </summary>
        public static object AttachScript(JObject @params)
        {
            string objectName = (string)@params["object_name"] ?? throw new System.Exception("Parameter 'object_name' is required.");
            string scriptName = (string)@params["script_name"] ?? throw new System.Exception("Parameter 'script_name' is required.");

            // Find the target object
            GameObject targetObject = GameObject.Find(objectName);
            if (targetObject == null)
                throw new System.Exception($"Object '{objectName}' not found in scene.");

            // Ensure script name ends with .cs
            if (!scriptName.EndsWith(".cs"))
                scriptName += ".cs";

            // Find the script asset
            string[] guids = AssetDatabase.FindAssets(Path.GetFileNameWithoutExtension(scriptName));
            if (guids.Length == 0)
                throw new System.Exception($"Script '{scriptName}' not found in project.");

            // Get the script asset
            string scriptPath = AssetDatabase.GUIDToAssetPath(guids[0]);
            MonoScript scriptAsset = AssetDatabase.LoadAssetAtPath<MonoScript>(scriptPath);
            if (scriptAsset == null)
                throw new System.Exception($"Failed to load script asset: {scriptName}");

            // Get the script type
            System.Type scriptType = scriptAsset.GetClass();
            if (scriptType == null)
                throw new System.Exception($"Script '{scriptName}' does not contain a valid MonoBehaviour class.");

            // Add the component
            Component component = targetObject.AddComponent(scriptType);
            if (component == null)
                throw new System.Exception($"Failed to add component of type {scriptType.Name} to object '{objectName}'.");

            return new
            {
                message = $"Successfully attached script '{scriptName}' to object '{objectName}'",
                component_type = scriptType.Name
            };
        }
    }
}