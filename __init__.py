# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import os

from bpy.props import StringProperty, BoolProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

from . import readtck


bl_info = {
    "name" : "TrainTracts",
    "description": "An addon for the import and translation of brain tractography .TCK files into 3D objects.",
    "author" : "Athanasios Bourganos",
    "blender" : (3, 0, 0),
    "version" : (1, 0, 0),
    "location": "File > Import",
    "category": "Import-Export"
}


def create_tract(ob_name, coords, edges=[], faces=[]):
    """Create point cloud object based on given coordinates and name.

    Keyword arguments:
    ob_name -- new object name
    coords -- float triplets eg: [(-1.0, 1.0, 0.0), (-1.0, -1.0, 0.0)]
    """

    # Create new mesh and a new object
    me = bpy.data.meshes.new(ob_name + "Mesh")
    ob = bpy.data.objects.new(ob_name, me)

    # Make a mesh from a list of vertices/edges/faces
    me.from_pydata(coords, edges, faces)

    # Display name and update the mesh
    ob.show_name = True
    me.update()
    return ob


class OpenTCKFile(Operator, ImportHelper):

    bl_idname = "test.open_tck"
    bl_label = "Tractography (.tck)"
    bl_icon = 'SYSTEM'
    
    filter_glob: StringProperty(
        default='*.tck',
        options={'HIDDEN'}
    )
    
    is_verbose: BoolProperty(
        name='Verbose',
        description='Make file import verbose.',
        default=False,
    )

    decimate: IntProperty(
        name='Decimate Factor',
        description='Decimate tracts by 1/value (2 = half of tracks).',
        default=1,
        min=1, 
        max=100
    )

    def execute(self, context):
        """Do something with the selected file(s)."""
        
        header, tracts = readtck.readTCK(self.filepath, verbose=self.is_verbose)

        if self.is_verbose:
            t_count = str()
            for char in header['count']:
                if char.isdigit():
                    t_count += char
            t_count = int(int(t_count)/self.decimate)
            print('Header reading complete and file data open...')
        
        c_count = 0

        pydata = list()
        edgedata = list()

        for a in range(0, len(tracts), self.decimate):

            tract = tracts[a]

            c_count += 1

            if self.is_verbose and c_count % 10000 == 1:
                print(str((c_count/t_count)*100)+'%', 'of tracts prepared...')


            p_index = len(pydata)
            pydata += tract

            for _ in range(len(tract)-1):
                edgedata.append([p_index, p_index+1])
                p_index += 1

        # Create the object
        tract_obj = create_tract("tracts", pydata, edges=edgedata)
        
        # Link object to the active collection
        bpy.context.collection.objects.link(tract_obj)
        # bpy.ops.object.convert('CURVE')
        
        return {'FINISHED'}

def custom_draw(self, context):
    self.layout.operator("test.open_tck")

def register():
    bpy.utils.register_class(OpenTCKFile)
    bpy.types.TOPBAR_MT_file_import.append(custom_draw)


def unregister():
    bpy.utils.unregister_class(OpenTCKFile)


if __name__ == "__main__":
    register()