# Blender API imports
import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

# Importing the TCK file reader
from . import readtck


# TrainTracts Blender addon info
bl_info = {
    "name" : "TrainTracts",
    "description": "An addon for the import and translation of brain tractography .TCK files into 3D objects.",
    "author" : "Athanasios Bourganos",
    "blender" : (3, 0, 0),
    "version" : (1, 0, 0),
    "location": "File > Import",
    "category": "Import Export"
}


def create_tract(ob_name, coords, edges=[], faces=[]):
    '''
    Function for creating a new mesh from tract data
    Takes in object name, coordinates in format [(X1, Y1, Z1), (X2, Y2, Z2), ...],
    list of edges in format [[vert1, vert2], [vert2, vert3], ...], and list of faces
    in format [[vert1, vert2, vert3], ...] (No faces are used in TrainTracts plugin)
    '''

    # Create instance of mesh and object
    mesh = bpy.data.meshes.new(ob_name + "Mesh")
    obj = bpy.data.objects.new(ob_name, mesh)

    # Make the tractography mesh from a list of vertices/edges
    mesh.from_pydata(coords, edges, faces)

    # Don't display name and update the mesh in Blender
    obj.show_name = False
    mesh.update()
    return obj


class OpenTCKFile(Operator, ImportHelper):

    # Plugin operator info and label for the menu
    bl_idname = "test.open_tck"
    bl_label = "Tractography (.tck)"
    bl_icon = 'SYSTEM'
    
    # File filtering property in the file picker
    filter_glob: StringProperty(
        default='*.tck',
        options={'HIDDEN'}
    )
    
    # Property for setting import as verbose
    is_verbose: BoolProperty(
        name='Verbose',
        description='Make file import verbose.',
        default=False,
    )

    # Property for decimating the mesh by removing tracts
    # (1/decimate of the tracts will be used in the mesh)
    decimate: IntProperty(
        name='Decimate Factor',
        description='Decimate tracts by 1/value (2 = half of tracks).',
        default=1,
        min=1, 
        max=100
    )

    def execute(self, context):
        # Method to actually open the file, get the data, and make the mesh!
        
        # Open the file and extract the header and tracts
        header, tracts = readtck.readTCK(self.filepath, verbose=self.is_verbose)

        # If verbose then extract the tract count for progress messages
        if self.is_verbose:
            t_count = str()
            for char in header['count']:
                if char.isdigit():
                    t_count += char
            t_count = int(int(t_count)/self.decimate)
            print('Header reading complete and file data open...')
        
        # Define some important variables
        c_count = 0
        pydata = list()
        edgedata = list()

        # Iterate through the tracts and decimate if needed
        for a in range(0, len(tracts), self.decimate):

            # Set current tract and iterate count
            tract = tracts[a]
            c_count += 1

            # Some more talkative code with progress included...
            if self.is_verbose and c_count % 10000 == 1:
                print(str((c_count/t_count)*100)+'%', 'of tracts prepared...')

            # Some code that generates a list of edges within but not between tracts!
            # This will likely be the most underapreciated optimization in the code...
            p_index = len(pydata)
            pydata += tract

            for _ in range(len(tract)-1):
                edgedata.append([p_index, p_index+1])
                p_index += 1

        # Create the mesh from the vertices and edges
        tract_obj = create_tract("tracts", pydata, edges=edgedata)
        
        # Link object to the active collection
        bpy.context.collection.objects.link(tract_obj)
        
        # Finish the execution and send the finished message!
        return {'FINISHED'}


# Get the plugin akk setup as an operator
def custom_draw(self, context):
    self.layout.operator("test.open_tck")

# Register the plugin and display it in the file import menu
def register():
    bpy.utils.register_class(OpenTCKFile)
    bpy.types.TOPBAR_MT_file_import.append(custom_draw)

# Unregister the plugin if needed
def unregister():
    bpy.utils.unregister_class(OpenTCKFile)

# Start it all up when loaded!
if __name__ == "__main__":
    register()