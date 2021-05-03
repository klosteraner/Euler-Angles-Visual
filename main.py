import numpy as np
import warnings

from traits.api import HasTraits, Instance, Property, on_trait_change
from traitsui.api import View, Item, Group

from tvtk.pyface.scene_editor import SceneEditor

from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene

from AngleControl import AngleControlPanel
from TaitBryanRotation import camera_to_world_rotation_matrix, angles_yaw_pitch_roll, angles_pix4d_omega_phi_kappa
from WorldSystem import system_NED, system_ENU, camera_world_alignment_at_zero_photogrammetric
from draw_scene import draw_world_with_coordinate_system_at_origin, \
        world_origin_to_camera_origin, generate_aligned_camera_mesh, \
        initial_view_pix4d_omega_phi_kappa, initial_view_yaw_pitch_roll


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
            (np.deg2rad(self.angles.angle_applied_first.final), self.angles.angle_applied_first.definition),
            self.world_system)

    # 3D Viewer
    mayavi_scene = Instance(MlabSceneModel, ())
    view3d = Item('mayavi_scene', show_label=False, editor=SceneEditor(scene_class=MayaviScene))

    # Complete GUI
    view = View(view3d,
                Item('angles', style="custom", show_label=False),
                Group(Item('rotation_camera_to_world')),
                resizable=True)

    def __init__(self, _euler_angle_definition, world_system, camera_world_alignment_at_zero, initial_view, **traits):
        HasTraits.__init__(self)

        self.world_system = world_system
        self.camera_world_alignment_at_zero = camera_world_alignment_at_zero
        self.initial_view = initial_view

        # Setup euler angles definition specific control panel
        self.angles.angle_applied_first.definition  = _euler_angle_definition.angles_in_order_applied[0]
        self.angles.angle_applied_second.definition = _euler_angle_definition.angles_in_order_applied[1]
        self.angles.angle_applied_last.definition   = _euler_angle_definition.angles_in_order_applied[2]

    @on_trait_change('mayavi_scene.activated')
    def initialize_scene(self):
        # We setup the scene outside the constructor as mayavi can only
        # initialize certain scene elements (e.g. text3d) properly after a view
        # on it is open. https://mayavi.readthedocs.io/en/latest/building_applications.html

        self.camera_mesh = generate_aligned_camera_mesh(self.world_system, self.camera_world_alignment_at_zero)
        self.world_to_camera_translation = world_origin_to_camera_origin(world_system)

        self.camera3d = self.mayavi_scene.mlab.triangular_mesh(
            self.camera_mesh.x + self.world_to_camera_translation[0],
            self.camera_mesh.y + self.world_to_camera_translation[1],
            self.camera_mesh.z + self.world_to_camera_translation[2],
            self.camera_mesh.faces, opacity=0.5, representation='fancymesh', name='camera')

        draw_world_with_coordinate_system_at_origin(self.mayavi_scene, self.world_system)

        self.mayavi_scene.mlab.view(azimuth=initial_view[0], elevation=initial_view[1], roll=initial_view[2], distance=10)

    @on_trait_change('rotation_camera_to_world')
    def update_plot(self):

        # The orientation of the camera mesh will be updated on user input
        x_camera_in_world, y_camera_in_world, z_camera_in_world = \
            (self.rotation_camera_to_world.dot(np.array([self.camera_mesh.x, self.camera_mesh.y, self.camera_mesh.z])))
        self.camera3d.mlab_source.trait_set(x=x_camera_in_world + self.world_to_camera_translation[0],
                                            y=y_camera_in_world + self.world_to_camera_translation[1],
                                            z=z_camera_in_world + self.world_to_camera_translation[2])


if __name__ == '__main__':
    '''
    Version 1:  Visualize Euler Angles (YPR, Pix4D OPK) on simple camera mesh.

                Rotation angles can be entered on a large scale, and chosen
                via a slider on a smaller scale to explore the format of the
                corresponding rotation matrix as well as the cameras visual 3D pose
                w.r.t to an ENU world (scene).
    '''

    euler_angle_definition = angles_pix4d_omega_phi_kappa()
    world_system = system_ENU()
    initial_view = initial_view_pix4d_omega_phi_kappa()

    #euler_angle_definition = angles_yaw_pitch_roll()
    #world_system = system_NED()
    #initial_view = initial_view_yaw_pitch_roll()

    camera_world_alignment_at_zero = camera_world_alignment_at_zero_photogrammetric()

    # Numpy <-> Python string comparison problem not yet addressed in mayavi
    # https://stackoverflow.com/questions/40659212/futurewarning-elementwise-comparison-failed-returning-scalar-but-in-the-futur
    warnings.simplefilter(action='ignore', category=FutureWarning)
    visualization = Visualization(euler_angle_definition, world_system, camera_world_alignment_at_zero, initial_view)
    visualization.configure_traits()
