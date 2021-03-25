from traits.api import HasTraits, Enum

WorldAxis = Enum('North', 'South', 'East', 'West', 'Up', 'Down')


class WorldSystem(HasTraits):
    '''
    Navigation system definition.
    '''
    x_axis = WorldAxis()
    y_axis = WorldAxis()
    z_axis = WorldAxis()


def NEDSystem():
    world_system = WorldSystem()
    world_system.x_axis = 'North'
    world_system.y_axis = 'East'
    world_system.z_axis = 'Down'

    return world_system


def ENUSystem():
    world_system = WorldSystem()
    world_system.x_axis = 'East'
    world_system.y_axis = 'North'
    world_system.z_axis = 'Up'

    return world_system