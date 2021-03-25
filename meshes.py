from numpy import array, sin, cos, mgrid

import numpy as np

class TriangleMesh:
    '''
    Used to hold the camera data to be transformed via the UI
    '''
    def __init__(self, _x, _y, _z, _faces):
        self.x = _x
        self.y = _y
        self.z = _z
        self.faces = _faces


def generate_camera_mesh(width = 4, height = 3):
    '''
    Camera mesh living in ENU world (x=east, y=north, z=up) that
    - has origin at 0
    - looks down (directed in negative z)
    - image top is oriented north (directed in positive y, indicated bz extra vertex)
    - image right(from camera center) is oriented east (directed in positive x)
    This corresponds to opk = 0, following the official pix4d opk definition.

    The return x,y,z, faces define a triangle mesh and
    are meant to be used by mayavi's triangular_mesh()
    TODO: Better indicate camera coordinate system
    '''

    vertices = array([[0., 0., 0.],
                         [0.5, 0.5, -1.], [0.5, -0.5, -1.],
                         [-0.5, -0.5, -1.], [-0.5, 0.5, -1.],
                         [0., 0.6, -1.]])
    faces = array([[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1], [1, 4, 5]])

    x, y, z = vertices.T
    x_ratio = width / max(width,height)
    y_ratio = height / max(width, height)
    x *= x_ratio
    y *= y_ratio

    return TriangleMesh(x,y,z, faces)


def generate_ground_mesh(origin, dimensions):
    '''
    Object representing the ENU world scene using origin at the cameras.

    The return x,y,z define a surface function and
    are meant to be used by mayavi's surf()
    '''

    x,y = mgrid[origin[0] - dimensions[0] : origin[0] + dimensions[0] : 0.1,
                origin[1] - dimensions[1] : origin[1] + dimensions[1] : 0.1]
    z = origin[2] + dimensions[2] * cos(x)*sin(-3.*y)

    return x,y,z


def generate_cyllinder_mesh(r, cone=False):
    '''
    Cyllinder mesh with z=[0,1] with radius r
    or cone pointing up with max_r = r

    The return x,y,z are a structured mesh and
    are meant to be used by mayavi's mesh()
    '''

    z_start, z_end, z_steps = (0.,1., 10)
    theta_start, theta_end, theta_steps = (0., 2*np.pi, 10)

    dz = (z_end-z_start) / z_steps
    dtheta = (theta_end-theta_start) / theta_steps
    [z, theta] = np.mgrid[z_start:z_end+dz:dz, theta_start:theta_end+dtheta:dtheta]

    if(cone):
        x = r * (1-z) * sin(theta)
        y = r * (1-z) * cos(theta)
    else:
        x = r * sin(theta)
        y = r * cos(theta)

    return x,y,z

def generate_arrow_mesh(height = 1.):
    '''
    Arrow object, will be used as coordinate system indicator

    The return x,y,z are a structured mesh and
    are meant to be used by mayavi's mesh()
    '''

    # 1. cylinder z=[0,0.7]
    height_cyl = 0.7 * height
    x_cyl, y_cyl, z_cyl = generate_cyllinder_mesh(r=0.03)
    z_cyl = height_cyl * z_cyl

    # 2.  cone z= [0.7, 1]
    height_cone = 0.3 * height
    x_cone, y_cone, z_cone = generate_cyllinder_mesh(r=0.1, cone=True)
    z_cone = height_cyl + height_cone * z_cone

    return np.concatenate((x_cyl, x_cone), axis=0), np.concatenate((y_cyl, y_cone), axis=0), np.concatenate((z_cyl, z_cone), axis=0)


def z_axis_align(x,y,z, world_axis, origin=array([0,0,0])):
    '''
    Applies coordinate transformation on x,y,z,
    s.t. z axis is swapped with axis given by world_axis
    and the coordinates are translated to the origin.

    Used place the 3 coordinate system axes.
    '''

    # 1. Orientation
    if world_axis == 'Up':
        x_new = x
        y_new = y
        z_new = z
    elif world_axis == 'Down':
        x_new = x
        y_new = y
        z_new = -z
    elif world_axis == 'East':
        x_new = z
        y_new = y
        z_new = x
    elif world_axis == 'West':
        x_new = -z
        y_new = y
        z_new = x
    elif world_axis == 'North':
        x_new = x
        y_new = z
        z_new = y
    elif world_axis == 'South':
        x_new = x
        y_new = -z
        z_new = y

    # 2. Translation to world origin
    return origin[0] + x_new, origin[1] + y_new, origin[2] + z_new


def draw_ground(mayavi_scene, origin, dimensions):
    x, y, z = generate_ground_mesh(origin, dimensions)
    mayavi_scene.mlab.surf(x, y, z)


def draw_world_axis(mayavi_scene, world_axis, origin, system_dimension):
    '''
    Draw an axis of a world coordinate system using the array mesh
    '''
    x, y, z = generate_arrow_mesh(height = system_dimension)
    x, y, z = z_axis_align(x, y, z, world_axis=world_axis, origin=origin)
    mayavi_scene.mlab.mesh(x, y, z, colormap="bone")

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

    mayavi_scene.mlab.text3d(text_position[0], text_position[1], text_position[2], world_axis, scale=0.2*system_dimension)


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

    system_dimension = 1.3 * np.max(ground_dimensions)
    draw_world_axis(mayavi_scene, world_system.x_axis, ground_origin, system_dimension)
    draw_world_axis(mayavi_scene, world_system.y_axis, ground_origin, system_dimension)
    draw_world_axis(mayavi_scene, world_system.z_axis, ground_origin, system_dimension)
