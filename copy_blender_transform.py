bl_info = {
    "name": "Copy Transform to Clipboard",
    "author": "Nazake",
    "version": (1, 4),
    "blender": (4, 0, 0),
    "location": "3D Viewport > Sidebar (N) > Transform Copy",
    "description": "Copy the active object's transform to the clipboard (plain or Unreal Engine format)",
    "category": "Object",
}

import bpy
import math
from bpy.props import BoolProperty


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def blender_loc_to_ue(loc):
    # Blender (meters, RH) -> UE (cm, LH): convert units, negate Y
    return (loc.x * 100.0, -loc.y * 100.0, loc.z * 100.0)


def blender_scale_to_ue(scl):
    # Scale: no unit change, no negation (negating would mirror the mesh)
    return (scl.x, scl.y, scl.z)


def blender_rot_to_ue(obj):
    if obj.rotation_mode == 'QUATERNION':
        e = obj.rotation_quaternion.to_euler('XYZ')
    else:
        e = obj.rotation_euler
    roll  =  math.degrees(e.x)
    pitch = -math.degrees(e.y)
    yaw   =  math.degrees(e.z)
    return (roll, pitch, yaw)


def fmt_xyz(v):
    return f"(X={v[0]:.6f},Y={v[1]:.6f},Z={v[2]:.6f})"


def build_plain_lines(obj, scene):
    lines = []
    if scene.copy_transform_use_location:
        loc = obj.location
        lines.append(f"Location: ({loc.x:.6f}, {loc.y:.6f}, {loc.z:.6f})")
    if scene.copy_transform_use_rotation:
        if obj.rotation_mode == 'QUATERNION':
            rot = obj.rotation_quaternion
            lines.append(
                f"Rotation (Quaternion): "
                f"({rot.w:.6f}, {rot.x:.6f}, {rot.y:.6f}, {rot.z:.6f})"
            )
        else:
            rot = obj.rotation_euler
            lines.append(f"Rotation (Euler): ({rot.x:.6f}, {rot.y:.6f}, {rot.z:.6f})")
    if scene.copy_transform_use_scale:
        scl = obj.scale
        lines.append(f"Scale: ({scl.x:.6f}, {scl.y:.6f}, {scl.z:.6f})")
    return lines


def build_ue_lines(obj, scene):
    lines = []
    if scene.copy_transform_use_location:
        lines.append(fmt_xyz(blender_loc_to_ue(obj.location)))
    if scene.copy_transform_use_rotation:
        r, p, y = blender_rot_to_ue(obj)
        lines.append(f"(Roll={r:.6f},Pitch={p:.6f},Yaw={y:.6f})")
    if scene.copy_transform_use_scale:
        lines.append(fmt_xyz(blender_scale_to_ue(obj.scale)))
    return lines


# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------

class OBJECT_OT_copy_transform_clipboard(bpy.types.Operator):
    """Copy the active object's transform to the clipboard (plain format)"""
    bl_idname = "object.copy_transform_clipboard"
    bl_label = "Copy to Clipboard"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        lines = build_plain_lines(obj, context.scene)
        if not lines:
            self.report({'WARNING'}, "Enable at least one channel (Location/Rotation/Scale)")
            return {'CANCELLED'}
        context.window_manager.clipboard = "\n".join(lines)
        self.report({'INFO'}, "Transform copied to clipboard")
        return {'FINISHED'}


class OBJECT_OT_copy_transform_clipboard_ue(bpy.types.Operator):
    """Copy the active object's transform to the clipboard in Unreal Engine format"""
    bl_idname = "object.copy_transform_clipboard_ue"
    bl_label = "Copy to Clipboard (Unreal)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        lines = build_ue_lines(obj, context.scene)
        if not lines:
            self.report({'WARNING'}, "Enable at least one channel (Location/Rotation/Scale)")
            return {'CANCELLED'}
        context.window_manager.clipboard = "\n".join(lines)
        self.report({'INFO'}, "UE transform copied to clipboard")
        return {'FINISHED'}


# ---------------------------------------------------------------------------
# Panel
# ---------------------------------------------------------------------------

class VIEW3D_PT_copy_transform_clipboard(bpy.types.Panel):
    bl_label = "Transform Copy"
    bl_idname = "VIEW3D_PT_copy_transform_clipboard"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transform Copy"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if obj is None:
            layout.label(text="No active object", icon='ERROR')
            return

        layout.label(text=f"Object: {obj.name}", icon='OBJECT_DATA')

        col = layout.column(align=True)
        col.prop(context.scene, "copy_transform_use_location", text="Location")
        col.prop(context.scene, "copy_transform_use_rotation", text="Rotation")
        col.prop(context.scene, "copy_transform_use_scale", text="Scale")

        layout.separator()

        col = layout.column(align=True)
        col.operator("object.copy_transform_clipboard", icon='COPYDOWN')
        col.operator("object.copy_transform_clipboard_ue", icon='COPYDOWN')


# ---------------------------------------------------------------------------
# Register / Unregister
# ---------------------------------------------------------------------------

classes = (
    OBJECT_OT_copy_transform_clipboard,
    OBJECT_OT_copy_transform_clipboard_ue,
    VIEW3D_PT_copy_transform_clipboard,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.copy_transform_use_location = BoolProperty(
        name="Location", description="Copy location", default=True,
    )
    bpy.types.Scene.copy_transform_use_rotation = BoolProperty(
        name="Rotation", description="Copy rotation", default=True,
    )
    bpy.types.Scene.copy_transform_use_scale = BoolProperty(
        name="Scale", description="Copy scale", default=True,
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.copy_transform_use_location
    del bpy.types.Scene.copy_transform_use_rotation
    del bpy.types.Scene.copy_transform_use_scale


if __name__ == "__main__":
    register()