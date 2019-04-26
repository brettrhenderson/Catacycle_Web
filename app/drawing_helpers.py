from matplotlib.path import Path
import math
import matplotlib.patches as patches
import numpy as np

def curved_arrow_single(theta1, theta2, radius, width, origin=(0,0), rel_head_width=0.5, rel_head_len=0.1,
                        abs_head_len=None, direction='cw'):
    """Construct the path for an irreversible arrow"""
    if direction == 'cw':
        a_angle = math.radians(theta1)

        # set the angle swept by the arrowhead
        if abs_head_len is None:    # compute arrow head length (angle swept) as a fraction of total length
            f_angle_offset = math.radians((theta2-theta1) * rel_head_len)
        else:
            f_angle_offset = abs_head_len

        # Define the radii of the inside and outside of the head and tail
        head_out_radius = radius + width / 2.0 + width*rel_head_width
        head_in_radius = radius - width / 2.0 - width*rel_head_width
        tail_out_radius = radius + width / 2.0
        tail_in_radius = radius - width / 2.0

        arrowhead_point = (radius * math.cos(a_angle), radius * math.sin(a_angle))
        head_out_point = (head_out_radius * math.cos(a_angle + f_angle_offset), head_out_radius * math.sin(a_angle + f_angle_offset))
        head_in_point = (head_in_radius * math.cos(a_angle + f_angle_offset), head_in_radius * math.sin(a_angle + f_angle_offset))

        # construct the path for the arrow using the above points and angles
        start = theta1 + math.degrees(f_angle_offset)
        outer_arc = scale_arc(Path.arc(start, theta2), tail_out_radius)
        inner_arc = scale_arc(path_arc_cw(theta2, start), tail_in_radius)
        arrowhead = join_points([head_in_point, arrowhead_point, head_out_point])

        return shift_path_by_vec(concatenate_paths([outer_arc, inner_arc, arrowhead]), np.array(origin))
    else:
        pass



def curved_arrow_double(theta1, theta2, radius, width_outer, width_inner, origin=(0,0), rel_head_width=0.5,
                        f_abs_head_len=None, r_abs_head_len=None, rel_head_len=0.1, direction='cw'):
    """Construct the paths a double-sided reversible arrow.

    Returns the paths for both the outer and inner arrows.
    Radius is the distance from the origin to the inside of the outer arrow"""
    if direction == 'cw':
        angle_point_out = math.radians(theta1)
        angle_point_in = math.radians(theta2)

        # set the angle swept by the arrowhead
        if f_abs_head_len is None:    # compute arrow head length (angle swept) as a fraction of total length
            f_angle_offset = math.radians((theta2-theta1) * rel_head_len)
        else:
            f_angle_offset = f_abs_head_len
        # set the angle swept by the arrowhead
        if r_abs_head_len is None:  # compute arrow head length (angle swept) as a fraction of total length
            r_angle_offset = math.radians((theta2 - theta1) * rel_head_len)
        else:
            r_angle_offset = r_abs_head_len

        # Define the radii of the inside and outside of the head and tail
        head_out_radius = radius + width_outer + width_outer * rel_head_width
        head_in_radius = radius - width_inner + width_inner * rel_head_width
        tail_out_radius = radius + width_outer
        tail_in_radius = radius - width_inner

        arrowtip_out_point = (radius * math.cos(angle_point_out), radius * math.sin(angle_point_out))
        arrowtip_in_point = (radius * math.cos(angle_point_in), radius * math.sin(angle_point_in))
        head_out_point = (head_out_radius * math.cos(angle_point_out + f_angle_offset), head_out_radius * math.sin(angle_point_out + f_angle_offset))
        head_in_point = (head_in_radius * math.cos(angle_point_in - f_angle_offset), head_in_radius * math.sin(angle_point_in - f_angle_offset))

        # construct the path for the outer arrow using the above points and angles
        start_outer_arc = theta1 + math.degrees(f_angle_offset)
        end_inner_arc = theta2 - math.degrees(f_angle_offset)
        outer_arc = scale_arc(Path.arc(start_outer_arc, theta2), tail_out_radius)
        middle_arc = scale_arc(path_arc_cw(theta2, theta1), radius)
        inner_arc = scale_arc(Path.arc(theta1, end_inner_arc), tail_in_radius)
        outer_arrowhead = join_points([arrowtip_out_point, head_out_point])
        inner_arrowhead = join_points([head_in_point, arrowtip_in_point])

        outer_path = shift_path_by_vec(concatenate_paths([outer_arc, middle_arc, outer_arrowhead]), np.array(origin))
        inner_path = shift_path_by_vec(concatenate_paths([middle_arc, inner_arc, inner_arrowhead]), np.array(origin))
        return outer_path, inner_path
    else:
        pass



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

def scale_arc(arc_path, scale):
    return Path(arc_path.vertices * scale, arc_path.codes)

def join_points(points):
    vertices = []
    codes = [Path.MOVETO]
    for i, (x,y) in enumerate(points):
        if i > 0:
            codes.append(Path.LINETO)
        vertices.append(np.array([x,y], float))
    return Path(np.array(vertices), codes)

def concatenate_paths(paths, connect=True):
    start_path = paths.pop(0)
    overall_verts = list(start_path.vertices)
    start_vert = tuple(overall_verts[0])
    overall_codes = list(start_path.codes)
    for path in paths:
        verts = list(path.vertices)
        codes = list(path.codes)
        if connect:
            codes[0] = Path.LINETO
        else:
            codes[0] = Path.MOVETO
        overall_codes += codes
        overall_verts += verts
    # close the path
    if connect:
        overall_verts.append(start_vert)
        overall_codes.append(Path.CLOSEPOLY)
    return Path(np.array(overall_verts), overall_codes)

def shift_path_by_vec(path, vec):
    shifted_vertices = np.array([vert + vec for vert in path.vertices])
    return Path(shifted_vertices, path.codes)
