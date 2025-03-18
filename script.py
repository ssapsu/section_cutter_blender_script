import bpy
import bmesh
import random
from mathutils import Vector

def create_cutter_from_polygon(points, z_min=-10000, z_max=10000):
    """
    주어진 2D 폐루프 (points)를 z축 방향으로 확장하여 cutter 오브젝트를 생성합니다.
    :param points: (x, y) 좌표의 리스트
    :param z_min: 하단 z값
    :param z_max: 상단 z값
    :return: 생성된 cutter 오브젝트
    """
    mesh = bpy.data.meshes.new("PolygonCutter")
    cutter_obj = bpy.data.objects.new("PolygonCutter", mesh)
    bpy.context.collection.objects.link(cutter_obj)

    bm = bmesh.new()

    bottom_verts = []
    top_verts = []
    for coord in points:
        x, y = coord
        bottom_verts.append(bm.verts.new(Vector((x, y, z_min))))
        top_verts.append(bm.verts.new(Vector((x, y, z_max))))

    bm.verts.ensure_lookup_table()

    try:
        bm.faces.new(bottom_verts)
    except Exception as e:
        print("하단 면 생성 오류:", e)

    try:
        bm.faces.new(top_verts[::-1])
    except Exception as e:
        print("상단 면 생성 오류:", e)

    n = len(points)
    for i in range(n):
        try:
            bm.faces.new([
                bottom_verts[i],
                bottom_verts[(i + 1) % n],
                top_verts[(i + 1) % n],
                top_verts[i]
            ])
        except Exception as e:
            print("측면 면 생성 오류:", e)

    bm.to_mesh(mesh)
    bm.free()

    bpy.context.view_layer.objects.active = cutter_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    cutter_obj.display_type = 'WIRE'
    cutter_obj.hide_render = True

    return cutter_obj

def create_sphere(location, radius=1, name="Sphere"):
    """
    주어진 위치와 반지름으로 UV 스피어를 생성합니다.
    :param location: (x, y, z) 좌표
    :param radius: 구의 반지름
    :param name: 오브젝트 이름
    :return: 생성된 구 오브젝트
    """
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    sphere = bpy.context.active_object
    sphere.name = name
    return sphere

def apply_boolean_modifier(obj, cutter_obj, operation='INTERSECT', solver='EXACT'):
    """
    obj에 cutter_obj를 이용한 boolean modifier (교차 연산)를 추가합니다.
    :param obj: boolean 연산을 적용할 오브젝트
    :param cutter_obj: cutter 역할을 하는 오브젝트
    :param operation: boolean 연산 종류 ('INTERSECT' 등)
    :param solver: boolean solver ('EXACT' 추천)
    :return: 생성된 modifier
    """
    bool_mod = obj.modifiers.new(name="Boolean_Intersect", type='BOOLEAN')
    bool_mod.operation = operation
    bool_mod.object = cutter_obj
    bool_mod.solver = solver
    return bool_mod

def apply_boolean_to_all_scene_objects(cutter_obj, operation='INTERSECT', solver='EXACT'):
    """
    현재 씬의 모든 Mesh 오브젝트에 대해 cutter_obj를 이용한 boolean modifier를 적용합니다.
    단, cutter 오브젝트 자체는 제외합니다.
    :param cutter_obj: boolean 연산에 사용할 cutter 오브젝트
    :param operation: boolean 연산 종류 ('INTERSECT' 등)
    :param solver: boolean solver ('EXACT' 추천)
    """
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and obj != cutter_obj:
            apply_boolean_modifier(obj, cutter_obj, operation, solver)

# -------------------------------------------------
# 예제 실행
# 다각형 (예: 좌표를 직접 지정한 직사각형)
points = [
    (-5000, 2500),
    (0, 2500),
    (0, -2500),
    (-5000, -2500),
]
cutter = create_cutter_from_polygon(points)

# 씬의 모든 Mesh 오브젝트에 cutter를 이용한 boolean 연산 적용
apply_boolean_to_all_scene_objects(cutter)
