from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np

def curved_arrow_single(theta1, theta2, radius, width, rel_head_width=0.5, rel_head_len=0.1, direction='cw'):



def curved_arrow_double(theta1, theta2, radius, width, rel_head_width=0.5, rel_head_len=0.1, direction='cw'):


def path_arc_cw(theta1, theta2):
    """used if theta1 >= theta2"""
    # construct the normal arc ccw
    arc1 = Path.arc(theta2, theta1)

    # flip the vertices and control points
    verts = list(arc1.vertices[0::2])
    verts.reverse()
    controls = list(arc1.vertices[1::2])
    controls.reverse()
    new_verts = []
    for i in range(len(controls)):
        new_verts.append(verts[i])
        new_verts.append(controls[i])
    new_verts.append(verts[-1])
    return Path(np.array(new_verts), arc1.codes)
