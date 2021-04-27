from numpy import max, array, identity, dot

from meshes import generate_arrow_mesh, generate_ground_mesh, generate_camera_mesh


def w_c(world_axis, camera_axis):
    '''
    Computes an entry w_i*c_i of the transformation matrix
    that aligns camera and world coordinate system.
    T = [[ w_x*c_x, w_x*c_y, w_x*c_z],
         [ w_y*c_x, w_y*c_y, w_y*c_z],
         [ w_z*c_x, w_z*c_y, w_z*c_z]]
    '''

    if world_axis == camera_axis:
        return 1
    elif (world_axis == 'East' and camera_axis == 'West') or \
         (world_axis == 'West' and camera_axis == 'East') or \
         (world_axis == 'North' and camera_axis == 'South') or \
         (world_axis == 'South' and camera_axis == 'North') or \
         (world_axis == 'Up' and camera_axis == 'Down') or \
         (world_axis == 'Down' and camera_axis == 'Up'):
        return -1
    else:
        return 0


def camera_alignment_matrix(world_system, camera_world_alignment_at_zero):
    '''
    Computes the transformation matrix to align a camera system
     x-axis: camera right (looking through the camera)
     y-axis: camera top (indicated by extra triangle)
     z-axis: camera back
     with a given world system
    '''

    w = world_system
    c = camera_world_alignment_at_zero
    return array([[w_c(w.x_axis, c.x_axis), w_c(w.x_axis, c.y_axis), w_c(w.x_axis, c.z_axis)],
                  [w_c(w.y_axis, c.x_axis), w_c(w.y_axis, c.y_axis), w_c(w.y_axis, c.z_axis)],
                  [w_c(w.z_axis, c.x_axis), w_c(w.z_axis, c.y_axis), w_c(w.z_axis, c.z_axis)]])


def world_origin_to_camera_origin(world_system, distance = 3):

    if world_system.x_axis == 'Up':
        return [distance, 0, 0]
    elif world_system.x_axis == 'Down':
        return [-distance, 0, 0]
    if world_system.y_axis == 'Up':
        return [0, distance, 0]
    elif world_system.y_axis == 'Down':
        return [0, -distance, 0]
    if world_system.z_axis == 'Up':
        return [0, 0, distance]
    elif world_system.z_axis == 'Down':
        return [0, 0, -distance]


def generate_aligned_camera_mesh(world_system, camera_world_alignment_at_zero):
    '''
    Returns camera mesh for a custom world system and camera world alignment.
    TODO: Better indicate camera coordinate system
    '''

    camera_mesh = generate_camera_mesh()
    T = camera_alignment_matrix(world_system, camera_world_alignment_at_zero)
    camera_mesh.x, camera_mesh.y, camera_mesh.z = dot(T, array([camera_mesh.x, camera_mesh.y, camera_mesh.z]))

    return camera_mesh


def draw_ground_at_origin(mayavi_scene, world_system, dimensions):
    '''
    Draw a surface representing the ground with adjusted z-axis
    such that plane is horizontal in world system (i.e. Up/Down orthogonal).
    '''

    x, y, z = generate_ground_mesh(dimensions)
    if world_system.x_axis in ['Up', 'Down']:
        x_new = z
        y_new = y
        z_new = x
    elif world_system.y_axis in ['Up', 'Down']:
        x_new = x
        y_new = z
        z_new = y
    elif world_system.z_axis in ['Up', 'Down']:
        x_new = x
        y_new = y
        z_new = z

    mayavi_scene.mlab.mesh(x_new, y_new, z_new)


def draw_coordinate_system_at_origin(mayavi_scene, world_system, axis_length):
    '''
    Draw a coordinate system that aligns wiht mayavis x,y,z system
    but with axis labels corresponding to the world system definition
    '''

    x,y,z = generate_arrow_mesh(axis_length)

    mayavi_scene.mlab.text3d(axis_length, 0, 0, world_system.x_axis, scale=0.2*axis_length)
    mayavi_scene.mlab.mesh(z, x, y, colormap="bone")

    mayavi_scene.mlab.text3d(0, 0, axis_length, world_system.z_axis, scale=0.2*axis_length)
    mayavi_scene.mlab.mesh(x, y, z, colormap="bone")

    mayavi_scene.mlab.text3d(0, axis_length, 0, world_system.y_axis, scale=0.2*axis_length)
    mayavi_scene.mlab.mesh(y, z, x, colormap="bone")


def draw_world_with_coordinate_system_at_origin(mayavi_scene, world_system, ground_dimensions = [1., 1., 0.2]):
    '''
    Draw world.
    To visualize the world we draw a ground mesh and coordinate system indicator.
    There can be several navigation systems we want to display (ENU, NED),
    but we want the scene to look the same, only with flipped system indicators.
    So for the visual scene system we choose ENU convention (it both makes live
    a little easier and also having z axis looking up (not down) seems intuitive
    for the visualization)
    '''

    draw_ground_at_origin(mayavi_scene, world_system, ground_dimensions)

    axes_length = 1.3 * max(ground_dimensions)
    draw_coordinate_system_at_origin(mayavi_scene, world_system, axes_length)
