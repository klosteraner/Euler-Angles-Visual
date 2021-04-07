import numpy as np

from traits.api import HasTraits, Instance, Property, on_trait_change
from traitsui.api import View, Item, Group

from tvtk.pyface.scene_editor import SceneEditor

from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene

from AngleControl import AngleControlPanel
from TaitBryanRotation import camera_to_world_rotation_matrix, yawPitchRollAngles, pix4dOmegaPhiKappaAngles
from WorldSystem import NEDSystem, ENUSystem
from meshes import generate_camera_mesh
from draw_scene import draw_world_with_coordinate_system

class Visualization(HasTraits):
    '''
    Visualization class.
    It holds the scene and takes care of the correspondence of
    UI elements (slider) and 3D visualization.
    '''

    # Rotation variables:
    angles = Instance(AngleControlPanel, ())
    rotation_camera_to_world = Property(observe='angles:angle_applied_first:final, '
                                                'angles:angle_applied_second:final, '
                                                'angles:angle_applied_last:final')
    def _get_rotation_camera_to_world(self):
        return camera_to_world_rotation_matrix(
            (np.deg2rad(self.angles.angle_applied_last.final), self.angles.angle_applied_last.definition),
            (np.deg2rad(self.angles.angle_applied_second.final), self.angles.angle_applied_second.definition),
            (np.deg2rad(self.angles.angle_applied_first.final), self.angles.angle_applied_first.definition))

    # 3D Viewer
    mayavi_scene = Instance(MlabSceneModel, ())
    view3d = Item('mayavi_scene', show_label=False, editor=SceneEditor(scene_class=MayaviScene))

    # Complete GUI
    view = View(view3d,
                Item('angles', style="custom", show_label=False),
                Group(Item('rotation_camera_to_world')),
                resizable=True)

    def __init__(self, _euler_angle_definition, world_system, **traits):
        HasTraits.__init__(self)

        # To make calculations easy the camera will be located at [0,0,0]
        self.camera_mesh = generate_camera_mesh()
        self.camera3d = self.mayavi_scene.mlab.triangular_mesh(
            self.camera_mesh.x, self.camera_mesh.y, self.camera_mesh.z, self.camera_mesh.faces,
            opacity=0.5, representation='fancymesh', name='camera')

        # And a world system at [0,0,3]
        ground_origin = [0, 0, -3]
        ground_dimensions = [1., 1., 0.2]
        draw_world_with_coordinate_system(self.mayavi_scene, world_system, ground_origin, ground_dimensions)

        # Setup euler angles definition specific control panel
        self.angles.angle_applied_first.definition  = _euler_angle_definition.angles_in_order_applied[0]
        self.angles.angle_applied_second.definition = _euler_angle_definition.angles_in_order_applied[1]
        self.angles.angle_applied_last.definition   = _euler_angle_definition.angles_in_order_applied[2]


    @on_trait_change('rotation_camera_to_world')
    def update_plot(self):

        # The orientation of the camera mesh will be updated on user input
        x_camera_in_world, y_camera_in_world, z_camera_in_world = \
            (self.rotation_camera_to_world.dot(np.array([self.camera_mesh.x, self.camera_mesh.y, self.camera_mesh.z])))
        self.camera3d.mlab_source.trait_set(x=x_camera_in_world, y=y_camera_in_world, z=z_camera_in_world)


if __name__ == '__main__':
    '''
    Version 1:  Visualize Euler Angles (YPR, Pix4D OPK) on simple camera mesh.

                Rotation angles can be entered on a large scale, and chosen
                via a slider on a smaller scale to explore the format of the
                corresponding rotation matrix as well as the cameras visual 3D pose
                w.r.t to an ENU world (scene).
    '''

    #euler_angle_definition = pix4dOmegaPhiKappaAngles()
    #world_system = ENUSystem
    euler_angle_definition = yawPitchRollAngles()
    world_system = NEDSystem()

    visualization = Visualization(euler_angle_definition, world_system)
    visualization.configure_traits()
