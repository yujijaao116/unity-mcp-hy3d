using System;
using Newtonsoft.Json;

namespace UnityMcpBridge.Editor.Models
{
    [Serializable]
    public class McpConfigServers
    {
        [JsonProperty("unityMCP-HY3D")]
        public McpConfigServer unityMCP;
    }
}
