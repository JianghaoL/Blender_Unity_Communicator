import json
import os
import socket
import bpy

bl_info = {
    "name": "Unity Communicator",
    "author": "Jianghao Li",
    "description": "Communicates with Unity to import mesh.",
    "blender": (4, 5, 3),
    "version": (1, 0, 0),
    "location": "View3D > Tools",
    "warning": "",
}


class OBJECT_OT_Export_Mesh_Command(bpy.types.Operator):
    "Export to Unity"
    bl_idname = "object.export_mesh_command"
    bl_label = "Export to Unity"
    bl_description = "Export to Unity"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        tempFolderPath = context.scene.selected_project_path

        if (not tempFolderPath.endswith("Assets")):
            folderPath = os.path.join(tempFolderPath, "Assets")

        folderPath += "\\" + context.scene.entered_model_name + ".fbx"

        bpy.ops.export_scene.fbx(
            filepath = folderPath,
            check_existing = True,
            use_selection = context.scene.should_export_selected_object_only,
        )

        self.report({'INFO'}, f"Exported to {folderPath}")
        return {'FINISHED'}


class OBJECT_OT_Get_Project_Path_Browser_Command(bpy.types.Operator):
    bl_idname = "object.get_project_path"
    bl_label = "Get Unity Path"
    bl_description = "Get Unity Path"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        context.scene.selected_project_path = self.directory
        return {'FINISHED'}


class OBJECT_OT_Get_Overwrite_Object_in_Unity_Command(bpy.types.Operator):
    bl_idname = "object.get_overwrite_object_in_unity"
    bl_label = "Get Object Path"

    filePath: bpy.props.StringProperty(
        name = "Selected Path",
        description = "Path to the selected object in Unity project",
        subtype = "FILE_PATH",
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        context.scene.selected_object_path = self.filePath
        return {'FINISHED'}

class OBJECT_OT_Overwrite_All_Objects_Command(bpy.types.Operator):
    bl_idname = "object.overwrite_all_objects_command"
    bl_label = "Overwrite Objects in Unity"
    bl_description = ("Overwrite Objects that uses this mesh in Unity. "
                      "\nBe careful! This will overwrite all objects in Unity that uses this mesh. Only use this when you are sure to do it!")
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        command = ["OverwriteAllObjects", context.scene.selected_object_path, context.scene.entered_model_name]
        send_command(command)
        return {'FINISHED'}

class VIEW3D_PT_Panel(bpy.types.Panel):
    bl_label = "Unity Communicator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unity Communicator"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "selected_project_path", text = "Unity Project Path")

        layout.separator()

        layout.prop(context.scene, "entered_model_name", text = "File Name")
        layout.prop(context.scene, "should_export_selected_object_only", text = "Export Selected Only")
        layout.operator(OBJECT_OT_Export_Mesh_Command.bl_idname)

        layout.separator()
        layout.prop(context.scene, "selected_object_path", text = "Object Path")
        layout.operator(OBJECT_OT_Overwrite_All_Objects_Command.bl_idname)


classes = [
    VIEW3D_PT_Panel,
    OBJECT_OT_Get_Project_Path_Browser_Command,
    OBJECT_OT_Export_Mesh_Command,
    OBJECT_OT_Overwrite_All_Objects_Command]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.selected_project_path = bpy.props.StringProperty(
        name = "Selected Path",
        description = "Path to the selected Unity project folder",
        subtype = "DIR_PATH"
    )

    bpy.types.Scene.entered_model_name = bpy.props.StringProperty(
        name="Model",
        description="Name of the model",
    )

    bpy.types.Scene.should_export_selected_object_only = bpy.props.BoolProperty(
        name = "Export Selected Only",
        description = "Export Selected Object Only",
    )

    bpy.types.Scene.selected_object_path = bpy.props.StringProperty(
        name = "Object Path",
        description = "Path to the selected object in Unity project",
        subtype = "FILE_PATH"
    )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.selected_project_path
    del bpy.types.Scene.should_export_selected_object_only
    del bpy.types.Scene.entered_model_name
    del bpy.types.Scene.selected_object_path


#####################################################################################

## This function is used to communicate with Unity
def send_command(cmd, IP = 5005):
    data = json.dumps(cmd)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", IP))
    s.sendall(data.encode("utf-8"))
    s.close()