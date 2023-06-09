import bpy
import os
import re
import shutil

CUSTOM_ADDON_NAME = 'Release Game'
"""
check this methods:

bpy.ops.wm.save_as_mainfile()
bpy.ops.wm.open_mainfile(filepath=fname)
bpy.ops.file.pack_all()

"""

size_items = [
    ("254", "254", "254"), 
    ("512", "512", "512"),
    ("1024", "1024", "1024")
]

def _addLoggedin(value):
    print('[Ok]',value)
    
def getOperatorName(action):
    return str(CUSTOM_ADDON_NAME.replace(" ", "_") + "." + action).lower()

class ReleaseBuildOperator(bpy.types.Operator):
    bl_idname = getOperatorName("build")
    bl_label = "Export game engine files and core, and prepare runtime to export into BPPlayer"
    
    def execute(self, context):
        errors = []
        print("======================Build Game=================================")
        SOURCE_PATH = bpy.path.abspath(context.scene.source_path)
        RELEASE_PATH = bpy.path.abspath(context.scene.release_path)
        UPBGE_PATH = bpy.path.abspath(context.scene.upbge_path)
        BPEX_FILE = bpy.path.abspath(context.scene.bpplayer_example)
        BPGUI_FILE = bpy.path.abspath(context.scene.bpplayer_gui)
        
        # validations
        if not context.scene.source_name:
            errors.append("Game name is required")
        if not os.path.exists(BPGUI_FILE):
            errors.append("BPPlayerGUI.exe not found")
        if not os.path.exists(BPEX_FILE):
            errors.append("BPPlayer.exe not found")
        
        if len(errors) > 0:
            self.report({"ERROR"}, ", ".join(errors))
            return {"FINISHED"}
        
        BUILD_PATH = os.path.join(RELEASE_PATH, context.scene.source_name)
        
        source_names = ["readme.md", "storage", "steam_appid.txt"]
        app_id_file = os.path.join(UPBGE_PATH, source_names[2])
        blender_player = os.path.join(UPBGE_PATH, 'blenderplayer.exe')

        if not os.path.exists(blender_player):
            self.report({"ERROR"}, "blenderplayer not found, check if the 'upbge_path' is valid")
            return {"FINISHED"}
        
        if os.path.exists(BUILD_PATH):
            shutil.rmtree(BUILD_PATH)
            _addLoggedin(f"Removed old {context.scene.source_name}")
        
        shutil.copytree(UPBGE_PATH, BUILD_PATH, ignore=shutil.ignore_patterns("*.txt", "*.html", "blender.exe"))
        _addLoggedin("Copyed UPBGE")
        
        if os.path.exists(app_id_file):
            shutil.copyfile(app_id_file, os.path.join(BUILD_PATH, source_names[2]))
            _addLoggedin(f"Copyed {source_names[2]}")

        if os.path.exists(SOURCE_PATH):
            readme_file = os.path.join(SOURCE_PATH, source_names[0])
            storage_file = os.path.join(SOURCE_PATH, source_names[1])
            if os.path.exists(readme_file):
                shutil.copyfile(readme_file, os.path.join(BUILD_PATH, source_names[0]))
                _addLoggedin(f"Copyed {source_names[0]}")
            if os.path.exists(storage_file):
                shutil.copytree(storage_file, os.path.join(BUILD_PATH, source_names[1]), ignore=shutil.ignore_patterns("*.db", "*.dat", "*.log"))
                _addLoggedin(f"Copyed {source_names[1]}")

        shutil.copyfile(BPEX_FILE, os.path.join(BUILD_PATH, f"{context.scene.source_name}.exe"))
        _addLoggedin(f"Created {context.scene.source_name}.exe")
        
        self.report({"INFO"}, "Build Game Completed")

        os.startfile(BPGUI_FILE)
        
        if context.scene.rehacker_gui:
            RHGUI_FILE = bpy.path.abspath(context.scene.rehacker_gui)
            if os.path.exists(RHGUI_FILE):
                os.startfile(RHGUI_FILE)

        return {"FINISHED"}

class PrepareBuildOperator(bpy.types.Operator):
    bl_idname = getOperatorName("prepare")
    bl_label = "Refresh the python scripts into a .blend project, and resize images for predefined sizes"
    
    def execute(self, context):
        SOURCE_PATH = bpy.path.abspath(context.scene.source_path)
        scale = int(context.scene.image_size)
        files = os.listdir(SOURCE_PATH)
        scriptReloads = 0
        scriptImports = 0
        imagesResizes = 0
        print("=======================Prepare Game================================")
        
        _addLoggedin("Scripts")
        for script in files:
            if re.search("\.py$", script):
                with open(SOURCE_PATH + script, 'r') as f:
                    extraMessage='Reloaded'
                    if not script in bpy.data.texts:
                        extraMessage='Imported'
                        scriptImports += 1
                        bpy.data.texts.new(script)
                    else:
                        scriptReloads += 1
                        bpy.data.texts[script].clear()
                    bpy.data.texts[script].write(f.read())
                    _addLoggedin(f"[-] {extraMessage} {script}")
        
        if context.scene.resize_image and scale:
            _addLoggedin("Images")
            for img in bpy.data.images:
                if re.search("sprite", img.name):
                    _addLoggedin(f'[-] {img.name} Skipped')
                    continue
                if img.size[0] == img.size[1] and img.size[0] > scale:
                    imagesResizes += 1
                    _addLoggedin(f"[-] {img.name}[{img.size[0]} x {img.size[1]}] Resized [{scale} x {scale}]")
                    img.scale(scale, scale)
                    img.pack(True)
        
        self.report({"INFO"}, f"{scriptReloads} Scripts reloaded, {scriptImports} Scripts imported, {imagesResizes} images resized")
        
        return {"FINISHED"}
    
class CompressBuildOperator(bpy.types.Operator):
    bl_idname = getOperatorName("compress")
    bl_label = "Create zip file for the game released"
    
    def execute(self, context):
        print("=======================Compress Game================================")
        RELEASE_PATH = bpy.path.abspath(context.scene.release_path)
        _build_file_data = os.path.join(RELEASE_PATH, context.scene.source_name, 'data.block')
        if os.path.exists(_build_file_data):
            build_path = os.path.join(RELEASE_PATH, context.scene.source_name)
            if os.path.exists(f"{build_path}.zip"):
                os.remove(f"{build_path}.zip")
                _addLoggedin(f"Removed old {context.scene.source_name}.zip")
            shutil.make_archive(build_path, 'zip', build_path)
            self.report({"INFO"}, f"Generated {context.scene.source_name}.zip")
        else:
            self.report({"ERROR"}, f"Please export game with bpplayer")
        
        return {"FINISHED"}

class ReleaseGamePanel(bpy.types.Panel):
    bl_label = CUSTOM_ADDON_NAME
    bl_idname = "PROPERTIES_" + str(CUSTOM_ADDON_NAME).replace(" ", "_")
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout 
        scene = context.scene
        # filepath = context.blend_data.filepath
        row = layout.row()
        col = row.column()
        
        col.separator()
        col.prop(scene, "source_name", text="Game name", icon="GAME")
        rowimg = col.row()
        rowimg.prop(scene, "resize_image", text="Resize images")
        if scene.resize_image:
            rowimg.prop(scene, "image_size", text="Size")
        
        col.separator()
        col.prop(scene, "upbge_path", text="Upbge path")
        col.prop(scene, "source_path", text="Source path")
        col.prop(scene, "release_path", text="Release path")
        col.prop(scene, "bpplayer_example", text="BPPlayer example")
        col.prop(scene, "bpplayer_gui", text="Bpplayer exe")
        col.prop(scene, "rehacker_gui", text="ReHacker exe")
        
        col.separator()
        row2 = col.row()
        row2.operator(getOperatorName("prepare"), text="Step 1 Prepare", icon="IMPORT")
        row2.operator(getOperatorName("build"), text="Step 2 Release", icon="EXPORT")

        col.separator()
        col.operator(getOperatorName("compress"), text="Step 3 Generate a zipfile")

classes = (
    ReleaseGamePanel,
    PrepareBuildOperator,
    ReleaseBuildOperator,
    CompressBuildOperator
)
bl_info = {
    "name": "Release Game",
    "description": "Publishing the .blend as runtime integrating with bpplayer",
    "author": "Marlon Cardoso (Mardozux Studio)",
    "version": (2, 0, 0),
    "blender": (2, 79, 0),
    "location": "Render Properties > Release Game",
    "wiki_url": "https://github.com/MRCardoso/upbge-utils/wiki/Addon-Release-Game",
    "category": "Game Engine"
}

def _read_paths():
    app_id_file = os.path.join(os.getcwd(), 'release_game.txt')
    default_paths = [str(os.getcwd()), "", "", ""]
    if os.path.isfile(app_id_file):
        with open(app_id_file, 'r') as f:
            default_values = [line.rstrip() for line in f]
            for i, l in enumerate(default_values):
                default_paths[i] = str(l)
    return default_paths

def register():
    for obj in classes:
        bpy.utils.register_class(obj)
        
    rg_paths = _read_paths()
    bpy.types.Scene.source_name = bpy.props.StringProperty(default="")
    bpy.types.Scene.upbge_path = bpy.props.StringProperty(default=rg_paths[0], subtype='DIR_PATH')
    bpy.types.Scene.source_path = bpy.props.StringProperty(default="", subtype='DIR_PATH')
    bpy.types.Scene.release_path = bpy.props.StringProperty(default="", subtype='DIR_PATH')
    
    bpy.types.Scene.resize_image = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.image_size = bpy.props.EnumProperty(items=size_items, default=size_items[1][0], name="Sizes")
    
    bpy.types.Scene.bpplayer_example = bpy.props.StringProperty(default=rg_paths[1], subtype='FILE_PATH')
    bpy.types.Scene.bpplayer_gui = bpy.props.StringProperty(default=rg_paths[2], subtype='FILE_PATH')
    bpy.types.Scene.rehacker_gui = bpy.props.StringProperty(default=rg_paths[3], subtype='FILE_PATH')
    

def unregister():
    for obj in classes:
        bpy.utils.unregister_class(obj)
    del bpy.types.Scene.bpplayer_example
    del bpy.types.Scene.source_name
    del bpy.types.Scene.source_path
    del bpy.types.Scene.upbge_path
    del bpy.types.Scene.release_path
    del bpy.types.Scene.resize_image
    del bpy.types.Scene.image_size
    del bpy.types.Scene.bpplayer_gui
    del bpy.types.Scene.rehacker_gui