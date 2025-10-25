using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

[InitializeOnLoad]
public static class BlenderCommunicator
{
    private static GameObject selectedObject;
    private static GameObject newObject;

    private static Thread listenerThread;
    private static TcpListener listener;

    private static bool running = false;

    static BlenderCommunicator()
    {
        StartServer();
    }

    private static void StartServer()
    {
        Debug.Log("Starting BlenderCommunicator...");
        if (running) return;
        running = true;

        listenerThread = new Thread(() =>
        {
            try
            {
                listener = new TcpListener(IPAddress.Loopback, 5005);
                listener.Start();
                Debug.Log("BlenderCommunicator: Listening on port 5005...");

                while (running)
                {
                    using (var client = listener.AcceptTcpClient())
                    using (var stream = client.GetStream())
                    {
                        byte[] buffer = new byte[2048];
                        int bytesRead = stream.Read(buffer, 0, buffer.Length);
                        string json = Encoding.UTF8.GetString(buffer, 0, bytesRead);

                        Debug.Log($"BlenderCommunicator: Received raw JSON: {json}");

                        HandleJsonArray(json);
                    }
                }
            }
            catch (SocketException e)
            {
                Debug.LogError("BlenderCommunicator socket error: " + e.Message);
            }
        });

        listenerThread.IsBackground = true;
        listenerThread.Start();
    }

    private static void HandleJsonArray(string json)
    {
        try
        {
            string[] commands = JsonUtilityWrapper.FromJson<string>(json);
            Debug.Log("BlenderCommunicator: Parsed JSON array with " + commands.Length + " elements.");
            EditorApplication.delayCall += () =>
            {
                string absolutePath;
                string relativePath;
                string name;

                // Selected Object
                absolutePath = commands[1];
                relativePath = absolutePath.Substring(absolutePath.IndexOf("Assets\\"));
                selectedObject = AssetDatabase.LoadAssetAtPath<GameObject>(relativePath);
                Debug.Log($"Selected Object path: {relativePath}");

                // New Object
                name = commands[2];
                relativePath = "Assets\\" + name + ".fbx";

                newObject = AssetDatabase.LoadAssetAtPath<GameObject>(relativePath);
                Debug.Log($"New Object path: {relativePath}");

                // Handle Command
                HandleCommand(commands[0]);

            };
        }
        catch (System.Exception e)
        {
            Debug.LogError("BlenderCommunicator: Error parsing JSON array: " + e.Message);
        }
    }

    private static void HandleCommand(string command)
    {
        switch (command)
        {
            case "OverwriteAllObjects":
                EditorApplication.delayCall += () => OverwriteAllObjects();
                break;
            default:
                Debug.LogWarning($"BlenderCommunicator: Unknown command '{command}'");
                break;
        }
    }

    private static void OverwriteAllObjects()
    {
        int replacedCount = 0;
        GameObject[] referencingMeshes = MonoBehaviour.FindObjectsByType<GameObject>(FindObjectsSortMode.None);
        foreach (GameObject go in referencingMeshes)
        {
            GameObject sourcePrefab = PrefabUtility.GetCorrespondingObjectFromSource(go);

            if (sourcePrefab == selectedObject)
            {

                Transform parent = go.transform.parent;
                Vector3 pos = go.transform.localPosition;
                Quaternion rot = go.transform.localRotation;
                Vector3 scale = go.transform.localScale;

                Undo.RegisterFullObjectHierarchyUndo(go, "Replace FBX");
                Undo.DestroyObjectImmediate(go);

                GameObject newInstance = (GameObject)PrefabUtility.InstantiatePrefab(newObject);

                if (parent)
                    newInstance.transform.SetParent(parent, false);
                newInstance.transform.localPosition = pos;
                newInstance.transform.localRotation = rot;
                newInstance.transform.localScale = scale;

                Undo.RegisterCreatedObjectUndo(newInstance, "Replace FBX");
                replacedCount++;
            }
        }
        Debug.Log($"BlenderCommunicator: OverwriteAllObjects executed. Replaced {replacedCount} instances.");
        EditorSceneManager.MarkAllScenesDirty();
    }

    [MenuItem("BlenderCommunicator/Stop Server")]
    private static void StopServer()
    {
        running = false;

        listener?.Stop();
        listenerThread?.Abort();

        Debug.Log("BlenderCommunicator stopped.");
    }
}

public static class JsonUtilityWrapper
{
    public static T[] FromJson<T>(string json)
    {
        string newJson = "{ \"Items\": " + json + "}";
        Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(newJson);
        return wrapper.Items;
    }

    [Serializable]
    private class Wrapper<T> { public T[] Items; }
}
