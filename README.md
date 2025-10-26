# Blender_Unity_Communicator
This is a Blender and Unity add-on that helps developers easily export models to the designated Unity project folder, and also provides a function to overwrite all objects using a specific .FBX model with the newly exported .FBX model.

## How to Set Up?
### On Blender Side
Add the python script `Blender_Unity_Communicator` the way you would when adding an add-on!

**Specifically, here is how you can set it up:**
First, go to the `Add-ons` tab
`Edit >> Preferences >> Add-ons`

Then, find the drop-down icon on the top-right corner of the window.

Finally, select `Install from Disk...` and select the python file.

### On Unity Side
Simply import the C-sharp script `BlenderCommunicator`

## How to Use?
### Exporting in Blender
When you finish setting up the add-on, you should see a tab show up on the side of the screen. 

**You can find it in __3D Viewport__ only**

You need to either enter the Unity project path manually or select the project using the file browser.

***Your path should lead to the top level of your Unity project***

Here is an example path:

`"E:\Unity Projects\TestProject"`

The add-on will automatically direct all its exported files to the Assets folder - don't worry about that!

After filling in the project path, you can export your models in the scene.

To export a model, you will first need to name it. **You do __NOT__ need to specify file extension name. It will automatically give it a .FBX extension**

Then you can toggle the checkbox to say whether you want to export only the selected object or the whole scene.

Finally, click `Export to Unity`, and you should see your model in the Assets folder!

### Overwrite Objects in Unity
> Try to do whiteboxing in a modeling software is a pain in the butt -- and I'm aware of it!

That's why there is this `Overwrite Objects in Unity` button.

This will help you replace all objects using an older model with the one you just created, with transform unchanged.

To overwrite objects, you need to first select which of them you want to overwrite.
You can do this by either entering the object's file path manually or selecting the file using the file browser.
Then, when you are sure with what object to overwrite, click `Overwrite Objects in Unity`, and that's it!

***IMPORTANT: THIS WILL OVERWRITE ALL OBJECTS WITH THE OLDER MODEL. ONLY DO IT WHEN YOU ARE SURE ABOUT WHAT YOU ARE DOING***

## About
This is the 1.00 version of this add-on. There may be more features on the way. :)

I hope this add-on will help solve some problems regarding exporting art assets and Unity whiteboxing.

Please email me at `jianghaoli800@gmail.com` should there be any bugs or related problem.

Cheers!🍺



