from numpy import array, max

from meshes import generate_world_axis_mesh, generate_ground_mesh

def compute_axis_text_position(world_axis, origin, system_dimension):
    '''
    Draw an axis of a world coordinate system using the array mesh
    '''

    text_position = array(origin, dtype=float, copy=True)
    if world_axis == 'Up':
        text_position[2] += system_dimension
    elif world_axis == 'Down':
        text_position[2] -= system_dimension
    elif world_axis == 'East':
        text_position[0] = text_position[0] + system_dimension
    elif world_axis == 'West':
        text_position[0] = text_position[0] - system_dimension
    elif world_axis == 'North':
        text_position[1] = text_position[1] + system_dimension
    elif world_axis == 'South':
        text_position[1] = text_position[1] - system_dimension
    else:
        raise("invalid world_axis.")

    return text_position


def draw_ground(mayavi_scene, origin, dimensions):
    x, y, z = generate_ground_mesh(origin, dimensions)
    mayavi_scene.mlab.surf(x, y, z)


def draw_coordinate_axis(mayavi_scene, world_axis, origin, axis_length):
    x,y,z = generate_world_axis_mesh(world_axis, origin, axis_length)
    mayavi_scene.mlab.mesh(x, y, z, colormap="bone")
    text_position = compute_axis_text_position(world_axis, origin, axis_length)
    mayavi_scene.mlab.text3d(text_position[0], text_position[1], text_position[2], world_axis, scale=0.2*axis_length)


def draw_world_with_coordinate_system(mayavi_scene, world_system, ground_origin = [0, 0, -3], ground_dimensions = [1., 1., 0.2]):
    '''
    Draw world.
    To visualize the world we draw a ground mesh and coordinate system indicator.
    There can be several navigation systems we want to display (ENU, NED),
    but we want the scene to look the same, only with flipped system indicators.
    So for the visual scene system we choose ENU convention (it both makes live
    a little easier and also having z axis looking up (not down) seems intuitive
    for the visualization)
    '''

    draw_ground(mayavi_scene, ground_origin, ground_dimensions)

    axes_length = 1.3 * max(ground_dimensions)
    draw_coordinate_axis(mayavi_scene, world_system.x_axis, ground_origin, axes_length)
    draw_coordinate_axis(mayavi_scene, world_system.y_axis, ground_origin, axes_length)
    draw_coordinate_axis(mayavi_scene, world_system.z_axis, ground_origin, axes_length)
