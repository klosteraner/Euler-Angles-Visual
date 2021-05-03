from traits.api import HasTraits, Bool, Enum, List, Str

from numpy import array, cos, sin

class ElementalRotationDefinition(HasTraits):
    '''
    A definition of an elemental rotation and its angle's name
    '''
    angle_name = Str("undefined angle")
    axis = Enum('around_x', 'around_y', 'around_z')
    isClockwiseCameraSystemRotation = Bool(False)


class TaitBryanAnglesDefinition(HasTraits):
    '''
    Tait-Bryan angle rotations are defined by three rotation angles around
    the x,y & z-axis.
    The resulting rotation will be different according to
    1. The order in which the rotations are applied
    2. The rotation direction (clockwise vs. counter-clockwise)
    '''
    angles_in_order_applied = List(ElementalRotationDefinition)


def angles_yaw_pitch_roll():
    '''
    Returns a definition of the "Yaw, Pitch, Roll" Tait-Bryan angles set widespread in aerospace applications.
    '''
    definition = TaitBryanAnglesDefinition()
    # first roll is applied
    definition.angles_in_order_applied.append(
        ElementalRotationDefinition(angle_name="Roll", axis='around_x', isClockwiseCameraSystemRotation=False))
    # then pitch
    definition.angles_in_order_applied.append(
        ElementalRotationDefinition(angle_name="Pitch", axis='around_y', isClockwiseCameraSystemRotation=False))
    # then yaw
    definition.angles_in_order_applied.append(
        ElementalRotationDefinition(angle_name="Yaw", axis='around_z', isClockwiseCameraSystemRotation=False))

    return definition


def angles_pix4d_omega_phi_kappa():
    '''
    Returns a definition of the "Omega, Phi, Kappa" Tait-Bryan angles set used by pix4d.
    '''

    definition = TaitBryanAnglesDefinition()
    # first kappa is applied
    definition.angles_in_order_applied.append(
        ElementalRotationDefinition(angle_name="Kappa", axis='around_z', isClockwiseCameraSystemRotation=False))
    # then phi
    definition.angles_in_order_applied.append(
        ElementalRotationDefinition(angle_name="Phi", axis='around_y', isClockwiseCameraSystemRotation=False))
    # last omega
    definition.angles_in_order_applied.append(
        ElementalRotationDefinition(angle_name="Omega", axis='around_x', isClockwiseCameraSystemRotation=False))

    return definition


def camera_to_world_rotation_around_x(cc_angle = 0):
    '''
    Compute a rotation matrix that is used to transform
    a point in camera coordinates to a point in world coordinates.
    when the camera(system) rotates counter-clockwise.
    (Seeing the camera(system) as fixed, the rotation
    would transform points clockwise around its x axis)
    '''
    return array([[1.,   0.,             0.],
                  [0.,   cos(cc_angle),  -sin(cc_angle)],
                  [0.,   sin(cc_angle),  cos(cc_angle)]])


def camera_to_world_rotation_around_y(cc_angle = 0):
    '''
    Compute a rotation matrix that is used to transform
    a point in camera coordinates to a point in world coordinates.
    when the camera(system) rotates counter-clockwise.
    (Seeing the camera(system) as fixed, the rotation
    would transform points clockwise around its x axis)
    '''

    return array([[cos(cc_angle),    0., sin(cc_angle)],
                  [0.,               1., 0.],
                  [-sin(cc_angle),   0., cos(cc_angle)]])


def camera_to_world_rotation_around_z(cc_angle = 0):
    '''
    Compute a rotation matrix that is used to transform
    a point in camera coordinates to a point in world coordinates
    when the camera(system) rotates counter-clockwise.
    (Seeing the camera(system) as fixed, the rotation
    would transform points clockwise around its x axis)
    '''

    return array([[cos(cc_angle),    -sin(cc_angle), 0.],
                  [sin(cc_angle),    cos(cc_angle),  0.],
                  [0.,               0.,             1.]])


def world_angle(angle, world_axis):
    '''
    Correction on the angle for possibly inverted axes
    due to the world system definition (w.r.t. the mayavi world system)
    '''
    if(world_axis in ['Down', 'West', 'South']):
        angle = -angle
    return angle


def elemental_rotation(angle_and_definition, worldsystem):
    '''
    Returns an elemental rotation matrix that is used to transform
    a point in camera coordinates to a point in world coordinates
    given an euler angle and its definition.
    '''
    angle, definition = angle_and_definition
    if (definition.isClockwiseCameraSystemRotation):
        angle = -angle

    if definition.axis == 'around_x':
        return camera_to_world_rotation_around_x(world_angle(angle, worldsystem.x_axis))
    if definition.axis == 'around_y':
        return camera_to_world_rotation_around_y(world_angle(angle, worldsystem.y_axis))
    if definition.axis == 'around_z':
        return camera_to_world_rotation_around_z(world_angle(angle, worldsystem.z_axis))


def camera_to_world_rotation_matrix(first_angle_and_definition,
                                    second_angle_and_definition,
                                    last_angle_and_definition,
                                    world_system):
    '''
    Compute a rotation matrix that is used to transform
    a point in camera coordinates to a point in world coordinates
    given Tait-Bryan angles and their definition.

    Note: Matrices application order is opposite to reading order
    '''
    return elemental_rotation(last_angle_and_definition, world_system).dot(
            elemental_rotation(second_angle_and_definition, world_system)).dot(
                elemental_rotation(first_angle_and_definition, world_system))
