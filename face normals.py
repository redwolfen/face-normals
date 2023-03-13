bl_info = {
    "name": "RodlumNormals",
    "author": "Rodolf Guanco Lumampao",
    "description": "Correct normals.",
    "blender": (3, 0, 0),
    "version": (1, 0, 0),
    "location": "View3D > Sidebar > Check Normals",
    "warning": "",
    "doc_url": "",
    "category": "Mesh Normals",
}


import bpy

class CheckNormalsOperator1(bpy.types.Operator):
    """Check for inverted face normals"""
    bl_idname = "object.check_normals"
    bl_label = "Check Normals1"

    def execute(self, context):
        # get the active object
        obj = context.active_object

        # switch to object mode and deselect all
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        # select the object
        obj.select_set(True)
        context.view_layer.objects.active = obj

        # show face normals
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='EDIT')
#        bpy.context.space_data.overlay.show_face_normals = True

        # check for inverted normals
        inverted_normals = []
        for poly in obj.data.polygons:
            if poly.normal.z < 0:
                inverted_normals.append(poly.index)

        # prompt user if there are inverted normals
        if inverted_normals:
            message = "There are inverted normals on faces: "
            for i in inverted_normals:
                message += str(i+1) + ", "
            message = message[:-2]
            self.report({'WARNING'}, message)
        else:
            self.report({'INFO'}, "All normals are facing outwards.")

        return {'FINISHED'}

class CheckNormalsPanel1(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport"""
    bl_label = "Normals"
    bl_idname = "OBJECT_PT_check_normals_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Correct Normals'

    def draw(self, context):
        layout = self.layout
        
        # Add button to execute check normals operator
        layout.operator("object.check_normals", text="Correct Normals")

        # Add button to toggle face orientation
        layout.prop(context.space_data.overlay, "show_face_normals", text="Face Normal Lines")
        # Add button to toggle face orientation
        box = layout.box()
        box.prop(context.space_data.overlay, "show_face_orientation", text="Show Face normals")
        box.prop(context.space_data.overlay, "show_stats", text="Show Statistics")
        layout.operator("view3d.camera_to_view", text="Camera to View")

def register():
    bpy.utils.register_class(CheckNormalsOperator1)
    bpy.utils.register_class(CheckNormalsPanel1)

def unregister():
    bpy.utils.unregister_class(CheckNormalsOperator1)
    bpy.utils.unregister_class(CheckNormalsPanel1)

    
if __name__ == "__main__":
    register()
