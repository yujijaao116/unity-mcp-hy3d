using UnityEngine;
using UnityEditor;
using UnityEditor.Build.Reporting;
using Newtonsoft.Json.Linq;

/// <summary>
/// Handles editor control commands like undo, redo, play, pause, stop, and build operations.
/// </summary>
public static class EditorControlHandler
{
    /// <summary>
    /// Handles editor control commands
    /// </summary>
    public static object HandleEditorControl(JObject @params)
    {
        string command = (string)@params["command"];
        JObject commandParams = (JObject)@params["params"];

        switch (command.ToUpper())
        {
            case "UNDO":
                return HandleUndo();
            case "REDO":
                return HandleRedo();
            case "PLAY":
                return HandlePlay();
            case "PAUSE":
                return HandlePause();
            case "STOP":
                return HandleStop();
            case "BUILD":
                return HandleBuild(commandParams);
            case "EXECUTE_COMMAND":
                return HandleExecuteCommand(commandParams);
            default:
                return new { error = $"Unknown editor control command: {command}" };
        }
    }

    private static object HandleUndo()
    {
        Undo.PerformUndo();
        return new { message = "Undo performed successfully" };
    }

    private static object HandleRedo()
    {
        Undo.PerformRedo();
        return new { message = "Redo performed successfully" };
    }

    private static object HandlePlay()
    {
        if (!EditorApplication.isPlaying)
        {
            EditorApplication.isPlaying = true;
            return new { message = "Entered play mode" };
        }
        return new { message = "Already in play mode" };
    }

    private static object HandlePause()
    {
        if (EditorApplication.isPlaying)
        {
            EditorApplication.isPaused = !EditorApplication.isPaused;
            return new { message = EditorApplication.isPaused ? "Game paused" : "Game resumed" };
        }
        return new { message = "Not in play mode" };
    }

    private static object HandleStop()
    {
        if (EditorApplication.isPlaying)
        {
            EditorApplication.isPlaying = false;
            return new { message = "Exited play mode" };
        }
        return new { message = "Not in play mode" };
    }

    private static object HandleBuild(JObject @params)
    {
        string platform = (string)@params["platform"];
        string buildPath = (string)@params["buildPath"];

        try
        {
            BuildTarget target = GetBuildTarget(platform);
            if ((int)target == -1)
            {
                return new { error = $"Unsupported platform: {platform}" };
            }

            BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
            buildPlayerOptions.scenes = GetEnabledScenes();
            buildPlayerOptions.target = target;
            buildPlayerOptions.locationPathName = buildPath;

            BuildReport report = BuildPipeline.BuildPlayer(buildPlayerOptions);
            return new
            {
                message = "Build completed successfully",
                summary = report.summary
            };
        }
        catch (System.Exception e)
        {
            return new { error = $"Build failed: {e.Message}" };
        }
    }

    private static object HandleExecuteCommand(JObject @params)
    {
        string commandName = (string)@params["commandName"];
        try
        {
            EditorApplication.ExecuteMenuItem(commandName);
            return new { message = $"Executed command: {commandName}" };
        }
        catch (System.Exception e)
        {
            return new { error = $"Failed to execute command: {e.Message}" };
        }
    }

    private static BuildTarget GetBuildTarget(string platform)
    {
        BuildTarget target;
        switch (platform.ToLower())
        {
            case "windows": target = BuildTarget.StandaloneWindows64; break;
            case "mac": target = BuildTarget.StandaloneOSX; break;
            case "linux": target = BuildTarget.StandaloneLinux64; break;
            case "android": target = BuildTarget.Android; break;
            case "ios": target = BuildTarget.iOS; break;
            case "webgl": target = BuildTarget.WebGL; break;
            default: target = (BuildTarget)(-1); break; // Invalid target
        }
        return target;
    }

    private static string[] GetEnabledScenes()
    {
        var scenes = new System.Collections.Generic.List<string>();
        for (int i = 0; i < EditorBuildSettings.scenes.Length; i++)
        {
            if (EditorBuildSettings.scenes[i].enabled)
            {
                scenes.Add(EditorBuildSettings.scenes[i].path);
            }
        }
        return scenes.ToArray();
    }
}