
import bpy
import os
import re
CUSTOM_ADDON_NAME = "Component Worker"

def getOperatorName(action):
    return str(CUSTOM_ADDON_NAME.replace(" ", "_") + "." + action).lower()

def comment_script(file, value=''):
    if not value:
        return
    with open(file, "r") as f:
        content = f.read()
        content = re.sub(r'^(.*import .*'+value+'.*)$', r'# \1', content, flags=re.MULTILINE)
        content = re.sub(r'^(.*from .*'+value+'.* import .*)$', r'# \1', content, flags=re.MULTILINE)
    with open(file, "w") as f:
        f.write(content)

def uncomment_script(file, value=''):
    if not value:
        return
    with open(file, "r") as f:
        content = f.read()
        content = re.sub(r'^#\s*(.*import .*'+value+'.*)$', r'\1', content, flags=re.MULTILINE)
        content = re.sub(r'^#\s*(.*from .*'+value+'.* import .*)$', r'\1', content, flags=re.MULTILINE)
    with open(file, "w") as f:
        f.write(content)

class ComponentList(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Component",default="")
    path_value = bpy.props.StringProperty(name="Component",default="")

class ComponentListUI(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        script = item.name.rsplit('.', 1)
        layout.label(text=script[-1], translate=False, icon="GAME")
        layout.label(text=script[0], translate=False, icon="TEXT")

class AppendOperator(bpy.types.Operator):
    bl_idname = getOperatorName("add")
    bl_label = "Append a new Component to Object"
    
    def execute(self, context):
        nm = context.scene.component_list[context.scene.component_list_active]
        try:
            comment_script(nm.path_value, context.scene.upbge_libs)
            bpy.ops.logic.python_component_register(component_name=nm.name)
            uncomment_script(nm.path_value, context.scene.upbge_libs)
        except Exception as ex:
            uncomment_script(nm.path_value, context.scene.upbge_libs)
            print(f'Error: {ex}')
        
        return {"FINISHED"}

class ReloadAllComponentOperator(bpy.types.Operator):
    bl_idname = getOperatorName("reloadall")
    bl_label = "Reloads the components of all the objects in the Scene."
    
    def execute(self, context):
        updated = 0
        act = bpy.context.scene.objects.active
        print('------------------------------------')

        for obj in bpy.context.scene.objects:
            flag = obj.select
            
            obj.select = True
            bpy.context.scene.objects.active = obj
            
            for i, comp in enumerate(obj.game.components):
                try:
                    paths = comp.module.split('.')
                    paths[-1] = paths[-1]+".py"
                    if context.scene.upbge_libs == paths[0]:
                        local_path = os.path.join(os.getcwd(), "2.79", "python", "lib", *paths)
                    else:
                        local_path = os.path.abspath(os.path.dirname(bpy.data.filepath)) +"\\"+ paths[0]
                    comment_script(local_path, context.scene.upbge_libs)
                    bpy.ops.logic.python_component_reload(index = i)
                    updated += 1
                    uncomment_script(local_path, context.scene.upbge_libs)
                except Exception as ex:
                    uncomment_script(local_path, context.scene.upbge_libs)
                    print(f'Error: {ex}')
                
            obj.select = flag
            
        bpy.context.scene.objects.active = act
        
        print(f"{updated} Components updated!")
        return {"FINISHED"}
    
class ListAllComponentOperator(bpy.types.Operator):
    bl_idname = getOperatorName("allcomponents")
    bl_label = "Display log for all components in the game"
    
    def execute(self, context):
        print("----------Debug Components Start----------")
        sorted_items = []
        for obj in bpy.context.scene.objects:
            for i, comp in enumerate(obj.game.components):
                sorted_items.append({
                    "component": f'{comp.module}.{comp.name}',
                    "obj": obj.name
                })
                # print(f'Component: {comp.module}.{comp.name} - Obj {obj.name}')
        sorted_items = sorted(sorted_items, key=lambda obj: obj['component'])
        for x in sorted_items:
            print(f'Component: {x["component"]} - Obj {x["obj"]}')
        print("----------Debug Components End----------")
        return {"FINISHED"}

class ManageComponentOperator(bpy.types.Operator):
    bl_idname = getOperatorName("refresh")
    bl_label = "Component Worker List"
    
    def execute(self, context):
        scene = context.scene        
        scene.component_list.clear()
        
        blend_directory = os.path.dirname(bpy.data.filepath)
        absolute_path = os.path.abspath(blend_directory)
        files = [os.path.join(absolute_path, file) for file in os.listdir(absolute_path) if os.path.isfile(os.path.join(absolute_path, file))]
        if context.scene.upbge_libs:
            def list_python_scripts(directory):
                python_scripts = []
                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)

                    if os.path.isfile(item_path):
                        if item.endswith(".py"):
                            python_scripts.append(item_path)

                    elif os.path.isdir(item_path):
                        python_scripts.extend(list_python_scripts(item_path))

                return python_scripts
            
            lib_path = os.path.join(os.getcwd(), "2.79", "python", "lib", context.scene.upbge_libs)
            for x in list_python_scripts(lib_path):
                files.append(x)

        for file in files:
            if file[-3:] != ".py":
                continue
            with open(file, "r") as f:
                strTxt = f.read()
                if "bge.types.KX_PythonComponent" not in strTxt:
                    continue
                for line in strTxt.split("\n"):
                    if "bge.types.KX_PythonComponent" in line:
                        class_name = line.replace("class", "").replace(" ","").split("(")[0]
                        file_name = str(file).replace(blend_directory, '')
                        if context.scene.upbge_libs:
                            lib_path = os.path.join(os.getcwd(), "2.79", "python", "lib")
                            file_name = file_name.replace(lib_path, '')
                        file_name = file_name.replace('\\', '.')
                        if file_name.startswith('.'):
                            file_name = file_name[1:]
                        item = scene.component_list.add()
                        item.name = f"{file_name[:-3]}.{class_name}"
                        item.path_value = file
                
        return {"FINISHED"}

class UIPanel(bpy.types.Panel):
    bl_label = "Component Worker"
    bl_idname = "LOGIC_EDITOR_Util_Components"
    bl_space_type = 'LOGIC_EDITOR'
    bl_region_type = 'UI'
    bl_context = "scene"
 
    def draw(self, context):
        layout = self.layout 
        scene = context.scene
        row = layout.row()
        col = row.column()
        pie = col.column(True)
        col2 = pie.box().column()

        row = col2.row()

        row.prop(scene, "component_show", text="", icon=["TRIA_RIGHT","TRIA_DOWN"][scene.component_show], emboss=False)
        row.label(text="Components")
        if scene.component_show:
            col2.template_list("ComponentListUI", "component_list_ui", scene,"component_list", scene, "component_list_active")
            col2.separator()
        
        selected_name=''
        size_list = len(scene.component_list)
        if scene.component_list_active >= 0 and scene.component_list_active <= (size_list-1):
            selected_name = str(scene.component_list[scene.component_list_active].name).rsplit('.', 1)
            selected_name = selected_name[-1]
        col3 = col.box().column()
        col3.prop(scene, "upbge_libs", text="Upbge Libs")
        col3.operator(getOperatorName("reloadall"), text="Update linked components in scene", icon="SCRIPT")
        col3.operator(getOperatorName("refresh"), text="Update list of components", icon="FILE_REFRESH")
        col3.operator(getOperatorName("add"), text=f"Append: {selected_name}", icon="ZOOMIN")
        col3.operator(getOperatorName("allcomponents"), text="Debug Components", icon="PLAY")
        col3.separator()

bl_info = {
    "name": "Component Worker",
    "description": "Addon to handle component scripts",
    "author": "Marlon Cardoso (Mardozux Studio)",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "Logic Editor > Properties tab > Component Worker",
    "category": "Game Engine"
}


classes = (
    UIPanel,
    ComponentListUI,
    ComponentList,
    AppendOperator,
    ReloadAllComponentOperator,
    ListAllComponentOperator,
    ManageComponentOperator
)

def register():
    for obj in classes:
        bpy.utils.register_class(obj)

    bpy.types.Scene.component_list = bpy.props.CollectionProperty(type=ComponentList)
    bpy.types.Scene.component_list_active = bpy.props.IntProperty(name="Active Component Selection", default=0)
    bpy.types.Scene.component_show = bpy.props.BoolProperty(name="Show Components", default=False)
    bpy.types.Scene.upbge_libs = bpy.props.StringProperty(name="Custom Upbge Lib", default="")

def unregister():
    for obj in classes:
        bpy.utils.unregister_class(obj)
        
    del bpy.types.Scene.component_list
    del bpy.types.Scene. component_list_active
    del bpy.types.Scene.upbge_libs
    del bpy.types.Scene.component_show