import bpy
import os
import shutil
from urllib import request
from zipfile import ZipFile

achievement_items = [
    ("clean", "Clean Achievement", "Clean Achievement"),
    ("get", "Get Achievement", "Get Achievement"),
    ("set", "Set Achievement", "Set Achievement"),
]

stats_items = [
    ("get", "Get Stats", "Get Stats"),
    ("set", "Set Stats", "Set Stats"),
]

CUSTOM_ADDON_NAME = "Steam Worker"
UPBGE_PATH = os.getcwd()

def _addLoggedin(value):
    print('[Ok]',value)
    
def __clean_lib_cache(_basename):
    __cache_path = os.path.join(UPBGE_PATH, _basename)
    if os.path.exists(__cache_path):
        shutil.rmtree(__cache_path)
        _addLoggedin(f'remove {_basename}')
        
def getOperatorName(action):
    return str(CUSTOM_ADDON_NAME.replace(" ", "_") + "." + action).lower()

def installSteamworkPy(_version, app_id):
    url = f'https://github.com/philippj/SteamworksPy/archive/refs/tags/{_version}.zip'
    _base_name = f'SteamworksPy-{_version}'
    app_id_name = 'steam_appid.txt'
    dll_sdk_name = 'SteamworksPy64.dll'
    lib_py_name = 'steamworks'
    
    _addLoggedin(f'{_base_name} -> {url}')
    
    bge_sdk_dir = os.path.join(UPBGE_PATH, "2.79","python", "lib", lib_py_name)
    bge_dll_file = os.path.join(UPBGE_PATH, dll_sdk_name)
    bge_app_id_file = os.path.join(UPBGE_PATH, app_id_name)
    
    for c in [bge_sdk_dir, bge_dll_file, bge_app_id_file]:
        if os.path.exists(c):
            if os.path.isfile(c):
                os.remove(c)
            else:
                shutil.rmtree(c)
            _addLoggedin(f"remove {c}")
    
    __clean_lib_cache(_base_name)
    
    zip_path, _ = request.urlretrieve(url)
    with ZipFile(zip_path, "r") as f:
        f.extractall(UPBGE_PATH)
        py_lib_path = os.path.join(UPBGE_PATH, _base_name, lib_py_name)
        py_dll_file = os.path.join(UPBGE_PATH, _base_name, "redist", "windows", dll_sdk_name)
        
        if os.path.exists(py_lib_path):
            shutil.copytree(py_lib_path, bge_sdk_dir)
            _addLoggedin(f'copyed {lib_py_name} lib')
        
        if os.path.exists(py_dll_file):
            shutil.copyfile(py_dll_file, bge_dll_file)
            _addLoggedin(f'copyed {dll_sdk_name} file')
        
        fa = open(bge_app_id_file, "a")
        fa.write(app_id)
        fa.close()
        _addLoggedin(f'created {app_id_name} file example')
        __clean_lib_cache(_base_name)

def installSteamworkSdk(_version):
    _url = f'https://partner.steamgames.com/downloads/steamworks_sdk_{_version}.zip'
    _base_name = 'sdk'
    _exts = ['dll', 'lib']
    
    _addLoggedin(f'{_base_name} -> {_url}')
    __clean_lib_cache(_base_name)
    
    zip_path, _ = request.urlretrieve(_url)
    with ZipFile(zip_path, "r") as f:
        f.extractall(UPBGE_PATH)
        
        for ext in _exts:
            _cache_id = f'steam_api64.{ext}'
            _cache_target = os.path.join(UPBGE_PATH, _cache_id)
            _cache_origin = os.path.join(UPBGE_PATH, _base_name, "redistributable_bin", "win64", _cache_id)
            
            if os.path.exists(_cache_origin):
                shutil.copyfile(_cache_origin, _cache_target)
                _addLoggedin(f'copyed {_cache_id} files')
        
        __clean_lib_cache(_base_name)

def InitializeSdk():
    from steamworks import STEAMWORKS
    sdk = STEAMWORKS()
    sdk.initialize()
    return sdk

class SteamWorkerPanel(bpy.types.Panel):
    bl_label = CUSTOM_ADDON_NAME
    bl_idname = "PROPERTIES_"+ str(CUSTOM_ADDON_NAME).replace(" ", "_")
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout 
        scene = context.scene
        row = layout.row()
        col = row.column()
        
        if bpy.types.Scene.app_id[1]['default']:
            header = col.row()
            header.operator(getOperatorName("reinstall"), text="", text_ctxt="reinstall SteamworksPy", icon='CANCEL')
            header.label(text=f"APP ID: {bpy.types.Scene.app_id[1]['default']}")
            rowx = col.row()
            rowx.prop(scene, "stat_achievement_too", text="Achievements Too")
            rowx.operator(getOperatorName("stats_reset"), text="Reset Stats")
            col.separator()
            
            pie = col.column(True)
            col2 = pie.box().column()
            row2 = col2.row()
            
            row2.prop(scene, "achievement_show", text="", icon=["TRIA_RIGHT","TRIA_DOWN"][scene.achievement_show], emboss=False)
            row2.label(text="Achievements")
            
            if scene.achievement_show:
                col2 = col2.box().column()
                col2.prop(scene, "achievement_name", text="Name")
                col2.prop(scene, "achievement_actions", text="Action")
                col2.separator()
                col2r = col2.row()
                col2r.operator(getOperatorName("achievements_load"), text="Refresh", icon="FILE_REFRESH")
                col2r.operator(getOperatorName("achievements_invoke"), text="Invoke", icon="PLAY")
                
            pie = col.column(True)
            col3 = pie.box().column()
            row3 = col3.row()
            
            row3.prop(scene, "stat_show", text="", icon=["TRIA_RIGHT","TRIA_DOWN"][scene.stat_show], emboss=False)
            row3.label(text="Stats")
            if scene.stat_show:
                col3 = col3.box().column()
                col3.prop(scene, "stat_name", text="Name")
                col3.prop(scene, "stat_actions", text="Action")
                col3.prop(scene, "stat_value", text="Value")
                col3.separator()
                col3.operator(getOperatorName("stats_invoke"), text="Invoke")
        else:
            col.label(text=f"Please configure SteamworksPy", icon='ERROR')
            col.separator()
            col.prop(scene, "install_spy_version", text="SteamworksPy Version")
            col.prop(scene, "install_sdk_version", text="Steam Sdk Version")
            col.prop(scene, "install_id", text="App ID")
            col.separator()
            col.operator(getOperatorName("install"), text="Install", icon="FILE_REFRESH")

class InstallSetsOperator(bpy.types.Operator):
    bl_idname = getOperatorName("install")
    bl_label = "Install sdks for working with steam"
    
    def execute(self, context):
        try:            
            installSteamworkPy(context.scene.install_spy_version, context.scene.install_id)
            installSteamworkSdk(context.scene.install_sdk_version)
            bpy.types.Scene.app_id[1]['default'] = context.scene.install_id
            self.report({"INFO"}, f'Installed SteamworksPy successful')
        except Exception as ex:
            self.report({"ERROR"}, 'Error to install')
            print(ex)
            print('======================CHECK THE POSSIBLE CASES:======================')
            print('- Reopen UPBGE to reinstall SteamworksPy (because it\'s in use, to get/set achievements or stats)')
            print('- Make sure to be logged the STEAMWORKS panel')
            print('- The versions that you provided are invalid')
            print('======================CHECK THE POSSIBLE CASES:======================')
        
        return {"FINISHED"}

class ReInstallOperator(bpy.types.Operator):
    bl_idname = getOperatorName("reinstall")
    bl_label = "ReInstall SteamworksPy"
    
    def execute(self, context):
        bpy.types.Scene.app_id[1]['default'] = ""
        return {"FINISHED"}

class RefreshAcievementOperator(bpy.types.Operator):
    bl_idname = getOperatorName("achievements_load")
    bl_label = "Make integration with steam stats"
    
    def execute(self, context):
        sdk = InitializeSdk()
        if (sdk.UserStats.RequestCurrentStats() == True):
            items = []
            for x in range(sdk.UserStats.GetNumAchievements()):
                n = sdk.UserStats.GetAchievementName(x).decode("utf-8")
                items.append((n, n, n))
            
            bpy.types.Scene.achievement_name = bpy.props.EnumProperty(items=items, name="Achievement Keys")
            self.report({"INFO"}, f'{len(items)} Achievements founded')
        else:
            self.report({"ERROR"}, 'Failed to get stats')
        
        return {"FINISHED"}

class AchievementsOperator(bpy.types.Operator):
    bl_idname = getOperatorName("achievements_invoke")
    bl_label = "Make integration with steam achievement_list"
    
    def execute(self, context):
        if not context.scene.achievement_name:
            self.report({"ERROR"}, "Achievement Name required")
            return {"FINISHED"}
        sdk = InitializeSdk()
        name = str.encode(context.scene.achievement_name)
        if (sdk.UserStats.RequestCurrentStats() == True):
            if context.scene.achievement_actions == "clean":
                sdk.UserStats.ClearAchievement(name)
                value = sdk.UserStats.StoreStats()
            elif context.scene.achievement_actions == "get":
                value = sdk.UserStats.GetAchievement(name)
            elif context.scene.achievement_actions == "set":
                sdk.UserStats.SetAchievement(name)
                value = sdk.UserStats.StoreStats()
            
            self.report({"INFO"}, f'{context.scene.achievement_actions.capitalize()}Achievement({name}) -> {value}')
        else:
            self.report({"ERROR"}, "Failed to get stats")
        
        return {"FINISHED"}


class ResetStatsOperator(bpy.types.Operator):
    bl_idname = getOperatorName("stats_reset")
    bl_label = "Make integration with steam stats"
    
    def execute(self, context):
        sdk = InitializeSdk()
        if (sdk.UserStats.RequestCurrentStats() == True):
            value = sdk.UserStats.ResetAllStats(context.scene.stat_achievement_too)
            self.report({"INFO"}, f'ResetAllStats({context.scene.stat_achievement_too}) -> {value}')
        
        return {"FINISHED"}

class StatsOperator(bpy.types.Operator):
    bl_idname = getOperatorName("stats_invoke")
    bl_label = "Make integration with steam stats"
    
    def execute(self, context):
        if not context.scene.stat_name:
            self.report({"ERROR"}, 'Stat Name is required')
            return {"FINISHED"}
        sdk = InitializeSdk()
        name = str.encode(context.scene.stat_name)
        if (sdk.UserStats.RequestCurrentStats() == True):
            if context.scene.stat_actions == "get":
                value = sdk.UserStats.GetStatInt(name)
            elif context.scene.stat_actions == "set":
                sdk.UserStats.SetStat(name, context.scene.stat_value)
                value = sdk.UserStats.StoreStats()
            
            self.report({"INFO"}, f'{context.scene.stat_actions.capitalize()}Stat({name}) -> {value}')
        else:
            self.report({"ERROR"}, 'Failed to get stats')
        
        return {"FINISHED"}
    
bl_info = {
    "name": "Steam Worker",
    "description": "Addon to integrate with steam sdk by SteamworksPy lib",
    "author": "Marlon Cardoso (Mardozux Studio)",
    "version": (1, 1, 0),
    "blender": (2, 79, 0),
    "location": "Render Properties > Steam Worker",
    "wiki_url": "https://github.com/MRCardoso/upbge-utils/wiki/Addon-Steam-Worker",
    "category": "Game Engine"
}

classes = (
    SteamWorkerPanel,
    StatsOperator,
    AchievementsOperator,
    RefreshAcievementOperator,
    ResetStatsOperator,
    InstallSetsOperator,
    ReInstallOperator
)

def register():
    for obj in classes:
        bpy.utils.register_class(obj)
        
    app_id = ""
    install_id = '480'
    app_id_file = os.path.join(os.getcwd(), 'steam_appid.txt')
    if os.path.isfile(app_id_file):
        with open(app_id_file, 'r') as f:
            app_id	= str(int(f.read()))
            install_id = app_id

    bpy.types.Scene.app_id = bpy.props.StringProperty(default=app_id)
    bpy.types.Scene.install_spy_version = bpy.props.StringProperty(default='1.6.5')
    bpy.types.Scene.install_sdk_version = bpy.props.StringProperty(default='157')
    bpy.types.Scene.install_id = bpy.props.StringProperty(default=install_id)
    
    bpy.types.Scene.stat_name = bpy.props.StringProperty(default="")
    bpy.types.Scene.stat_show = bpy.props.BoolProperty(name="Show Stats", default=False)
    bpy.types.Scene.stat_value = bpy.props.IntProperty(default=0)
    bpy.types.Scene.stat_actions = bpy.props.EnumProperty(items=stats_items, name="Stats Action")
    bpy.types.Scene.stat_achievement_too = bpy.props.BoolProperty(name="Achievement Too", default=False)
    
    bpy.types.Scene.achievement_name = bpy.props.EnumProperty(items=[], name="Achievement Action")
    bpy.types.Scene.achievement_show = bpy.props.BoolProperty(name="Show Achievements", default=False)
    bpy.types.Scene.achievement_actions = bpy.props.EnumProperty(items=achievement_items, name="Achievement Action")
    
def unregister():
    for obj in classes:
        bpy.utils.unregister_class(obj)
    del bpy.types.Scene.app_id
    del bpy.types.Scene.install_spy_version
    del bpy.types.Scene.install_sdk_version
    del bpy.types.Scene.install_id
    
    del bpy.types.Scene.achievement_name
    del bpy.types.Scene.achievement_show
    del bpy.types.Scene.achievement_actions
    
    del bpy.types.Scene.stat_name
    del bpy.types.Scene.stat_value
    del bpy.types.Scene.stat_show
    del bpy.types.Scene.stat_actions
    del bpy.types.Scene.stat_achievement_too