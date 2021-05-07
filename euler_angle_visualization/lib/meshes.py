from numpy import array, sin, cos, mgrid

import numpy as np

class TriangleMesh:
    '''
    Used to hold the camera data to be transformed via the UI
    The data is intended for visualization via mayavi's triangular_mesh()
    '''
    def __init__(self, _x, _y, _z, _faces):
        self.x = _x
        self.y = _y
        self.z = _z
        self.faces = _faces


def generate_camera_mesh(width = 4, height = 3):
    '''
    Returns camera mesh with origin at (0,0,0) and
     x-axis: camera right (looking through the camera)
     y-axis: camera top (indicated by extra triangle)
     z-axis: camera back

    Note: This definition can be used with the OPK(ENU) convention.
    '''

    vertices = array([[0., 0., 0.],
                         [0.5, 0.5, -1.], [0.5, -0.5, -1.],
                         [-0.5, -0.5, -1.], [-0.5, 0.5, -1.],
                         [0., 0.6, -1.]])
    faces = array([[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1], [1, 4, 5]])

    x, y, z = vertices.T
    x_ratio = width / max(width, height)
    y_ratio = height / max(width, height)
    x *= x_ratio
    y *= y_ratio

    return TriangleMesh(x,y,z, faces)


def generate_ground_mesh(dimensions):
    '''
    Object representing the ENU world scene using origin at the cameras.

    The return x,y,z define a surface function and
    are meant to be used by mayavi's surf()
    '''

    x,y = mgrid[-dimensions[0] : dimensions[0] : 0.1,
                -dimensions[1] : dimensions[1] : 0.1]
    z = dimensions[2] * cos(x)*sin(-3.*y)

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
