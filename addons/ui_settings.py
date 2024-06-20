import bpy
from bpy_extras import object_utils

def _create_plane():
    vertices = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
    faces = [(0, 1, 2, 3)]
    return [vertices, [], faces]

def _create_empty():
    scale_factor = 1.0 
    vertices = [
        (0, 0, 0), 
        (scale_factor, 0, 0), 
        (scale_factor, scale_factor, 0), 
        (0, scale_factor, 0),
        (0, 0, scale_factor), 
        (scale_factor, 0, scale_factor), 
        (scale_factor, scale_factor, scale_factor), 
        (0, scale_factor, scale_factor)
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), 
        (3, 0), (4, 5), (5, 6), 
        (6, 7), (7, 4), (0, 4), 
        (1, 5), (2, 6), (3, 7)
    ]
    faces = []
    return [vertices, edges, faces]
    
def create_new_mesh(name='MyMesh', verticles=[], edges=[], faces=[]):
    mesh = bpy.data.meshes.new(name)

    mesh.from_pydata(verticles, edges, faces)
    mesh.update()
    obj = object_utils.object_data_add(bpy.context, mesh, operator=None)
    obj.select = True
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    return obj


# obj = create_new_mesh(*_create_empty())
## create_new_mesh(*_create_progress_bar()) music/sfx volume
## create_new_mesh(*_create_toggle()) fullscreen