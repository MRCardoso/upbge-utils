import bpy
import os

achievement_items = [
    ("clean", "Clean Achievement", "Clean Achievement"),
    ("get", "Get Achievement", "Get Achievement"),
    ("set", "Set Achievement", "Set Achievement"),
]

stats_items = [
    ("get", "Get Stats", "Get Stats"),
    ("set", "Set Stats", "Set Stats"),
]

def InitializeSdk():
    from steamworks import STEAMWORKS
    sdk = STEAMWORKS()
    sdk.initialize()
    return sdk

class SteamWorkerPanel(bpy.types.Panel):
    bl_label = "Steam Worker"
    bl_idname = "PROPERTIES_Steam_Worker"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout 
        scene = context.scene
        row = layout.row()
        col = row.column()
        
        if scene.app_id:
            col.label(text=f"APP ID: {scene.app_id}", icon='QUESTION')
            col.separator()
            rowx = col.row()
            rowx.prop(scene, "stat_clean_ach", text="Achievements Too")
            rowx.operator("reset_stats.run", text="Reset Stats")
        else:
            col.label(text=f"Please configure SteamWorkersPy", icon='ERROR')
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
            col2r.operator("achievements.load", text="Refresh", icon="FILE_REFRESH")
            col2r.operator("achievements.invoke", text="Invoke", icon="PLAY")
            
        pie = col.column(True)
        col3 = pie.box().column()
        row3 = col3.row()
        
        row3.prop(scene, "stat_show", text="", icon=["TRIA_RIGHT","TRIA_DOWN"][scene.stat_show], emboss=False)
        row3.label(text="Stats")
        if scene.stat_show:
            col3 = col3.box().column()
            col3.prop(scene, "stat_name", text="Name")
            col3.prop(scene, "stat_list", text="Action")
            col3.prop(scene, "stat_value", text="Value")
            col3.separator()
            col3.operator("achievements.stats", text="Invoke")

class RefreshAcievementOperator(bpy.types.Operator):
    bl_idname = "achievements.load"
    bl_label = "Make integration with steam stats"
    
    def execute(self, context):
        sdk = InitializeSdk()
        if (sdk.UserStats.RequestCurrentStats() == True):
            items = []
            for x in range(sdk.UserStats.GetNumAchievements()):
                n = sdk.UserStats.GetAchievementName(x).decode("utf-8")
                items.append((n, n, n))
            
            bpy.types.Scene.achievement_name = bpy.props.EnumProperty(items=items, name="Achievement Keys")
            self.report({"INFO"}, f'{len(items)} Achievement founded')
        else:
            self.report({"ERROR"}, 'Failed to get stats')
        
        return {"FINISHED"}

class ResetStatsOperator(bpy.types.Operator):
    bl_idname = "reset_stats.run"
    bl_label = "Make integration with steam stats"
    
    def execute(self, context):
        sdk = InitializeSdk()
        if (sdk.UserStats.RequestCurrentStats() == True):
            value = sdk.UserStats.ResetAllStats(context.scene.stat_clean_ach)
            self.report({"INFO"}, f'ResetAllStats({context.scene.stat_clean_ach}) -> {value}')
        
        return {"FINISHED"}    

class AchievementsOperator(bpy.types.Operator):
    bl_idname = "achievements.invoke"
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

class StatsOperator(bpy.types.Operator):
    bl_idname = "achievements.stats"
    bl_label = "Make integration with steam stats"
    
    def execute(self, context):
        if not context.scene.stat_name:
            self.report({"ERROR"}, 'Stat Name is required')
            return {"FINISHED"}
        sdk = InitializeSdk()
        name = str.encode(context.scene.stat_name)
        if (sdk.UserStats.RequestCurrentStats() == True):
            if context.scene.stat_list == "get":
                value = sdk.UserStats.GetStatInt(name)
            elif context.scene.stat_list == "set":
                sdk.UserStats.SetStat(name, context.scene.stat_value)
                value = sdk.UserStats.StoreStats()
            
            self.report({"INFO"}, f'{context.scene.stat_list.capitalize()}Stat({name}) -> {value}')
        else:
            self.report({"ERROR"}, 'Failed to get stats')
        
        return {"FINISHED"}
    
bl_info = {
    "name": "Steam Worker",
    "description": "Addon to test and integrate SteamworksPy sdk",
    "author": "Marlon Cardoso (Mardozux Studio)",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "Render Properties > Steam Worker",
    "category": "Game Engine"
}

classes = (
    SteamWorkerPanel,
    StatsOperator,
    AchievementsOperator,
    RefreshAcievementOperator,
    ResetStatsOperator
)

def register():
    for obj in classes:
        bpy.utils.register_class(obj)
        
    app_id = ""
    app_id_file = os.path.join(os.getcwd(), 'steam_appid.txt')
    if os.path.isfile(app_id_file):
        with open(app_id_file, 'r') as f:
            app_id	= str(int(f.read()))
    
    bpy.types.Scene.app_id = bpy.props.StringProperty(default=app_id)
    
    bpy.types.Scene.stat_name = bpy.props.StringProperty(default="")
    bpy.types.Scene.stat_show = bpy.props.BoolProperty(name="Show Stats", default=False)
    bpy.types.Scene.stat_value = bpy.props.IntProperty(default=0)
    bpy.types.Scene.stat_list = bpy.props.EnumProperty(items=stats_items, name="Stats Action")
    bpy.types.Scene.stat_clean_ach = bpy.props.BoolProperty(name="Achievement Too", default=False)
    
    bpy.types.Scene.achievement_name = bpy.props.EnumProperty(items=[], name="Achievement Action")
    bpy.types.Scene.achievement_show = bpy.props.BoolProperty(name="Show Achievements", default=False)
    bpy.types.Scene.achievement_actions = bpy.props.EnumProperty(items=achievement_items, name="Achievement Action")
    
def unregister():
    for obj in classes:
        bpy.utils.unregister_class(obj)
    del bpy.types.Scene.app_id
    
    del bpy.types.Scene.achievement_name
    del bpy.types.Scene.achievement_show
    del bpy.types.Scene.achievement_actions
    
    del bpy.types.Scene.stat_name
    del bpy.types.Scene.stat_value
    del bpy.types.Scene.stat_show
    del bpy.types.Scene.stat_list
    del bpy.types.Scene.stat_clean_ach