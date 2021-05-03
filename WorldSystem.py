from traits.api import HasTraits, Enum

WorldAxis = Enum('North', 'South', 'East', 'West', 'Up', 'Down')


class WorldSystem(HasTraits):
    '''
    Navigation system definition.
    '''
    x_axis = WorldAxis()
    y_axis = WorldAxis()
    z_axis = WorldAxis()


def system_NED():
    world_system = WorldSystem()
    world_system.x_axis = 'North'
    world_system.y_axis = 'East'
    world_system.z_axis = 'Down'

    return world_system


def system_ENU():
    world_system = WorldSystem()
    world_system.x_axis = 'East'
    world_system.y_axis = 'North'
    world_system.z_axis = 'Up'

    return world_system

def camera_world_alignment_at_zero_photogrammetric():
    '''
    Assuming the photogrammetric camera system:
    x-axis: camera right (looking through the camera)
    y-axis: camera top
    z-axis: camera back,
    the function returns the world axes that this camera system
    aligns with at (0,0,0)
    '''
    world_system = WorldSystem()
    world_system.x_axis = 'East'
    world_system.y_axis = 'North'
    world_system.z_axis = 'Up'

    return world_system