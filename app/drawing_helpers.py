from matplotlib.path import Path
import math
import matplotlib.patches as patches
import numpy as np
import matplotlib.path as mpath
import matplotlib.transforms as transforms
from functools import reduce
import logging

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)


def curved_arrow_single(theta1, theta2, radius, width, origin=(0,0), rel_head_width=1.5, rel_head_len=0.1,
                        abs_head_len=None, reverse=False):
    """Construct the path for an irreversible curved arrow"""
    # set the angle swept by the arrowhead
    if abs_head_len is None:  # compute arrow head length (angle swept) as a fraction of total length
        f_angle_offset = math.radians((theta2 - theta1) * rel_head_len)
    else:
        f_angle_offset = abs_head_len

    # Define the radii of the inside and outside of the head and tail
    head_width = width * rel_head_width
    tail_out_radius = radius + width / 2.0
    tail_in_radius = radius - width / 2.0

    if not reverse:
        theta_tip = theta1
        theta_tail = theta2

    else:
        theta_tip = theta2
        theta_tail = theta1
        f_angle_offset = -f_angle_offset

    # head_in_point, arrowhead_point, head_out_point = get_perp_arrowhead(radius, theta_tip, f_angle_offset, width, rel_head_width)
    head_in_point, arrowhead_point, head_out_point = get_isosceles_arrowhead(radius, math.radians(theta_tip),
                                                                             math.radians(theta_tip) + f_angle_offset,
                                                                             head_width)
    int_outer, ix_pts_outer = get_intersect_segment_circle(head_in_point, head_out_point, tail_out_radius)
    int_inner, ix_pts_inner = get_intersect_segment_circle(head_in_point, head_out_point, tail_in_radius)
    if int_outer:
        start = math.degrees(cart2pol(*ix_pts_outer[0])[1])
    else:
        start = theta_tip + math.degrees(f_angle_offset)
        # make head wider if it doesn't intersect both sides of tail
        # return curved_arrow_single(theta1, theta2, radius, width, origin, rel_head_width + 0.1, rel_head_len,
        #                 abs_head_len, reverse)
    if int_inner:
        end = math.degrees(cart2pol(*ix_pts_inner[0])[1])
    else:
        end = theta_tip + math.degrees(f_angle_offset)
        # make head wider if it doesn't intersect both sides of tail
        # return curved_arrow_single(theta1, theta2, radius, width, origin, rel_head_width + 0.1, rel_head_len,
        #                            abs_head_len, reverse)

    if not reverse:
        # print(f'THETATAIL: {theta_tail}, START: {start}, END: {end} THETATIP: {theta_tip}')
        while theta_tail <= end or theta_tail <= start or theta_tail - theta_tip <= math.degrees(f_angle_offset) + 0.5:
            theta_tail += 0.1

        outer_arc = scale_arc(Path.arc(start, theta_tail), tail_out_radius)
        inner_arc = scale_arc(path_arc_cw(theta_tail, end), tail_in_radius)
    else:
        # print(f'THETATAIL: {theta_tail}, START: {start}, END: {end} THETATIP: {theta_tip}')
        # while theta_tail >= end or theta_tail >= start or theta_tail - theta_tip >= math.degrees(f_angle_offset) + 0.5:
        #     theta_tail += 0.1
        outer_arc = scale_arc(path_arc_cw(start, theta_tail), tail_out_radius)
        inner_arc = scale_arc(Path.arc(theta_tail, end), tail_in_radius)
    arrowhead = join_points([head_in_point, arrowhead_point, head_out_point])

    return shift_path_by_vec(concatenate_paths([outer_arc, inner_arc, arrowhead]), np.array(origin))


def curved_arrow_double(theta1, theta2, radius, width_outer, width_inner, origin=(0,0), rel_head_width=1.5,
                        f_abs_head_len=None, r_abs_head_len=None, rel_head_len=0.1, reverse=False):
    """Construct the paths a double-sided reversible curved arrow.

    Returns the paths for both the outer and inner arrows.
    Radius is the distance from the origin to the inside of the outer arrow"""
    if not reverse:
        angle_tip_out = math.radians(theta1)
        angle_tip_in = math.radians(theta2)

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
        head_out_width = width_outer * (rel_head_width + 1)
        head_in_width = width_inner * (rel_head_width + 1)
        tail_out_radius = radius + width_outer
        tail_in_radius = radius - width_inner

        head_out_in_xy, arrowtip_out_xy, head_out_out_xy = get_isosceles_arrowhead(radius, angle_tip_out,
                                                                  angle_tip_out + f_angle_offset, head_out_width)
        head_in_in_xy, arrowtip_in_xy, head_in_out_xy = get_isosceles_arrowhead(radius, angle_tip_in,
                                                                angle_tip_in - r_angle_offset, head_in_width)

        int_outer, ix_pts_outer = get_intersect_segment_circle(head_out_in_xy, head_out_out_xy, tail_out_radius)
        int_inner, ix_pts_inner = get_intersect_segment_circle(head_in_in_xy, head_in_out_xy, tail_in_radius)
        if int_outer:
            start_outer_arc = math.degrees(cart2pol(*ix_pts_outer[0])[1])
        else:
            start_outer_arc = theta1 + math.degrees(f_angle_offset)
        if int_inner:
            end_inner_arc = math.degrees(cart2pol(*ix_pts_inner[0])[1])
        else:
            end_inner_arc = theta2 - math.degrees(r_angle_offset)

        outer_arc = scale_arc(Path.arc(start_outer_arc, theta2), tail_out_radius)
        middle_arc = scale_arc(path_arc_cw(theta2, theta1), radius)
        inner_arc = scale_arc(Path.arc(theta1, end_inner_arc), tail_in_radius)
        outer_arrowhead = join_points([head_out_out_xy])
        inner_arrowhead = join_points([head_in_in_xy])

        outer_path = shift_path_by_vec(concatenate_paths([outer_arc, middle_arc, outer_arrowhead]), np.array(origin))
        inner_path = shift_path_by_vec(concatenate_paths([middle_arc, inner_arc, inner_arrowhead]), np.array(origin))
        return outer_path, inner_path
    else:
        pass

def straight_arrow_single(length, width, origin=(0,0), rel_head_width=0.5,
                        abs_head_len=None, rel_head_len=0.2, reverse=False):
    """Construct the path for an irreversible straight arrow"""
    # set the width of the arrowhead
    if abs_head_len is None:  # compute arrow head length (angle swept) as a fraction of total length
        f_offset = length * rel_head_len
    else:
        f_offset = abs_head_len

    width_head_part = width * rel_head_width

    if reverse:
        length = -length
        f_offset = -f_offset

    tip = (length / 2, 0)
    start = (length / 2 - f_offset, width / 2)
    tail_top = (-length / 2, width / 2)
    tail_bottom = (-length / 2, -width / 2)
    head_bottom = (length / 2 - f_offset, -width / 2)
    head_bottom_point = (length / 2 - f_offset, - width_head_part / 2)
    head_top_point = (length / 2 - f_offset, width_head_part / 2)
    points = [start, tail_top, tail_bottom, head_bottom, head_bottom_point, tip, head_top_point]
    path = patches.Polygon(np.array(points)).get_path()
    return shift_path_by_vec(path, np.array(origin))


def straight_arrow_double(length, width_top, width_bottom, origin=(0,0), rel_head_width=0.5,
                        f_abs_head_len=None, r_abs_head_len=None, rel_head_len=0.2, reverse=False):
    """Construct the path for an irreversible straight arrow"""
    # set the width of the arrowhead
    if f_abs_head_len is None:  # compute arrow head length (angle swept) as a fraction of total length
        f_offset = length * rel_head_len
    else:
        f_offset = f_abs_head_len
    if r_abs_head_len is None:  # compute arrow head length (angle swept) as a fraction of total length
        r_offset = length * rel_head_len
    else:
        r_offset = r_abs_head_len

    width_head_top = width_top * rel_head_width
    width_head_bottom = width_bottom * rel_head_width

    if reverse:
        length = -length
        f_offset = -f_offset
        r_offset = -r_offset

    tip_top = (length / 2, 0)
    start = (length / 2 - f_offset, width_top)
    tail_top_top = (-length / 2, width_top)
    tail_bottom_top = (-length / 2, 0)
    head_top_point = (length / 2 - f_offset, width_head_top / 2 + width_top / 2)

    points_top = [start, tail_top_top, tail_bottom_top, tip_top, head_top_point]
    path_top = patches.Polygon(np.array(points_top)).get_path()

    tail_bottom_bottom = (length / 2, -width_bottom)
    head_bottom_bottom = (-length / 2 + r_offset, -width_bottom)
    head_bottom_point = (-length / 2 + r_offset, -width_bottom / 2 - width_head_bottom / 2)

    points_bottom = [tail_bottom_top, head_bottom_point, head_bottom_bottom, tail_bottom_bottom, tip_top]
    path_bottom = patches.Polygon(np.array(points_bottom)).get_path()

    return shift_path_by_vec(path_top, np.array(origin)), shift_path_by_vec(path_bottom, np.array(origin))


def filled_circular_arc(theta1, theta2, radius, width, origin=(0,0)):
    """Construct the path for a circular arc"""

    # Define the radii of the inside and outside of the arc
    out_radius = radius + width / 2.0
    in_radius = radius - width / 2.0

    outer_arc = scale_arc(Path.arc(theta1, theta2), out_radius)
    inner_arc = scale_arc(path_arc_cw(theta2, theta1), in_radius)

    return shift_path_by_vec(concatenate_paths([outer_arc, inner_arc]), np.array(origin))


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

def path_arc_smart(theta1, theta2):
    if theta1 >= theta2:
        return path_arc_cw(theta1, theta2)
    else:
        return Path.arc(theta1, theta2)

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

def set_ax_lims(ax, paths):
    bbox_pts = mpath.get_paths_extents(paths).get_points()
    max_x_dim = np.max(bbox_pts[:, 0])
    max_y_dim = np.max(bbox_pts[:, 1])
    min_x_dim = np.min(bbox_pts[:, 0])
    min_y_dim = np.min(bbox_pts[:, 1])
    xlim = (min_x_dim - 0.1, max_x_dim + 0.1)
    ylim = (min_y_dim - 0.5, max_y_dim + 0.1)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect(1)

def ensure_valid_gap(delta, gap, precision=1):
    theta1 = 90 - delta + (gap / 2.0)
    theta2 = 90 - (gap / 2.0)

    while theta2 <= theta1:
        gap -= precision
        theta1 = 90 - delta + (gap / 2.0)
        theta2 = 90 - (gap / 2.0)
    return gap

def ensure_valid_gaps(delta, gap1, gap0, precision=1):
    theta1 = 90 - delta + (gap1 / 2.0)
    theta2 = 90 - (gap0 / 2.0)

    while theta2 <= theta1:
        gap1 -= precision / 2
        gap0 -= precision / 2
        theta1 = 90 - delta + (gap1 / 2.0)
        theta2 = 90 - (gap0 / 2.0)
    return gap1, gap0

def ensure_all_valid_gaps(delta, gaps, precision=1):
    for i in range(len(gaps)):
        theta1 = 90 - delta + (gaps[i] / 2.0)
        theta2 = 90 - (gaps[i-1] / 2.0)

        while theta2 <= theta1:
            gaps[i] -= precision / 2
            gaps[i-1] -= precision / 2
            theta1 = 90 - delta + (gaps[i] / 2.0)
            theta2 = 90 - (gaps[i-1] / 2.0)
    return gaps

def get_isosceles_arrowhead(radius, theta1, theta2, base_width):
    point1 = radius * np.array([math.cos(theta1), math.sin(theta1)])
    point2 = radius * np.array([math.cos(theta2), math.sin(theta2)])
    v_12 = point2 - point1
    if v_12[0] == 0:    # vertical line.  We are at the right or left of the circle
        u_cross = np.array([1,0])
    elif v_12[1] == 0:
        u_cross = np.array([0, 1])
    else:
        u_cross = np.array([v_12[1], -v_12[0]]) / np.sqrt(v_12[1]**2 + v_12[0]**2)    # m expressed as unit vector
    point4 = point2 + base_width / 2 * u_cross
    point5 = point2 - base_width / 2 * u_cross

    if np.linalg.norm(point4) > np.linalg.norm(point5):
        return [point5, point1, point4]     # inside, tip, outside
    else:
        return [point4, point1, point5]     # inside, tip, outside

def get_isosceles_arrowhead_old(radius, theta1, theta2, base_width):
    point1 = radius * np.array([math.cos(theta1), math.sin(theta1)])
    point2 = radius * np.array([math.cos(theta2), math.sin(theta2)])
    if point1[0] == 0:    # vertical line.  We are at the top or bottom of the circle
        delx = point2[0] - point1[0]
        point3 = point1 + np.array([delx, 0])
        u_m = np.array([0,1])
    elif point1[1] == 0:
        dely = point2[1] - point1[1]
        point3 = point1 + np.array([0, dely])
        u_m = np.array([1, 0])
    else:
        m = math.sin(theta1)/math.cos(theta1)
        line1 = np.array([m, 0])    # m, b in y=mx+b
        line2 = np.array([m, point2[1] - m * point2[0]])    # || to line 1 but through point 2
        line3 = np.array([-1 / m, point1[1] + 1 / m * point1[0]])    # normal to lines 1 and 2 and through point 1
        point3_x = (line3[1] - line2[1]) / (m + 1 / m)
        point3 = np.array([point3_x, m * point3_x + line2[1]])    # intersection of line 3 and line 2
        u_m = np.array([1, m]) / np.sqrt(1**2 + m**2)    # m expressed as unit vector
    point4 = point3 + base_width / 2 * u_m
    point5 = point3 - base_width / 2 * u_m

    return [point5, point1, point4]     # inside, tip, outside

def get_perp_arrowhead(radius, theta_tip, f_angle_offset, width, rel_head_width, reverse):
    head_out_radius = radius + width / 2.0 + width * rel_head_width
    head_in_radius = radius - width / 2.0 - width * rel_head_width

    angle_tip = math.radians(theta_tip)

    arrowhead_point = (radius * math.cos(angle_tip), radius * math.sin(angle_tip))
    head_out_point = (head_out_radius * math.cos(angle_tip + f_angle_offset), head_out_radius * math.sin(angle_tip + f_angle_offset))
    head_in_point = (head_in_radius * math.cos(angle_tip + f_angle_offset), head_in_radius * math.sin(angle_tip + f_angle_offset))
    return [head_in_point, arrowhead_point, head_out_point]

def get_intersect_segment_circle(p1, p2, r, p_cent=np.array([0,0])):
    """https://codereview.stackexchange.com/questions/86421/line-segment-to-circle-collision-algorithm"""
    V = p2 - p1
    a = V.dot(V)
    b = 2 * V.dot(p1 - p_cent)
    c = p1.dot(p1) + p_cent.dot(p_cent) - 2 * p1.dot(p_cent) - r**2

    disc = b**2 - 4 * a * c
    if disc < 0:  # line misses circle
        return False, []
    else:
        t1 = (-b + np.sqrt(disc)) / (2 * a)
        t2 = (-b - np.sqrt(disc)) / (2 * a)
    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):    # line segment doesn't extend far enough to intersect circle
        return False, None
    else:
        pts = []
        for mult in [t1, t2]:
            if 0 <= mult <= 1:
                pts.append(p1 + mult * V)
        return True, pts

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    if phi > np.pi / 2:
        phi -= 2 * np.pi
    return rho, phi

def rotate_patches_about(ax, patches, theta, pt):
    """
    Rotate matplotlib patches about a point in data space
    :param ax: Axes on which to perform transformation
    :param patches: list of patches to rotate
    :param theta: float. angle to rotate by (in radians)
    :param pt: tuple. point to rotate about
    :return: None
    """
    t = transforms.Affine2D().rotate_around(pt[0], pt[1], theta)

    for patch in patches:
        # patch.set_transform(t + ax.transData)
        patch.set_transform(t + ax.transData)


def reflect_patches_about(ax, patches, var, val):
    """
    Reflect matplotlib patches about a vertical or horizontal line
    :param ax: Axes on which to perform transformation
    :param patches: list of patches to rotate
    :param var: int. the variable associated with val. 0 for x, 1 for y.
    :param val: float.  The value of the coordinate to reflect about.
            Example: if var == 0 and val = 2, reflect about the line x = 2.
    :return: None
    """
    t1 = transforms.Affine2D().translate(-val * (var == 0), -val*(var == 1))  # translate to reference either x- or y-axis
    t2 = transforms.Affine2D(np.array([[-1*(var == 0)*2+1, 0, 0],[0, -1*(var == 1)*2+1, 0], [0, 0, 1]]))  # reflect
    t3 = transforms.Affine2D().translate(val * (var == 0), val * (var == 1))  # re-translate back to original location

    for patch in patches:
        patch.set_transform(t1 + t2 + t3 + ax.transData)

def get_rotate_trans(theta, pt):
    """
    Get matplotlib.transform to rotate patches about a point in data space
    :param theta: float. angle to rotate by (in radians)
    :param pt: tuple. point to rotate about
    :return: matplotlib.transform
    """
    return transforms.Affine2D().rotate_around(pt[0], pt[1], theta)

def get_reflect_trans(var, val):
    """
    Get the matplotlib.transform that reflects about a vertical or horizontal line
    :param var: int. the variable associated with val. 0 for x, 1 for y.
        Example: if var == 0, the reflection will be about a vertical line
    :param val: float.  The value of the coordinate to reflect about.
            Example: if var == 0 and val = 2, reflect about the line x = 2.
    :return: None
    """
    t1 = transforms.Affine2D().translate(-val * (var == 0), -val * (var == 1))  # translate to reference either x- or y-axis
    t2 = transforms.Affine2D(np.array([[-1 * (var == 0) * 2 + 1, 0, 0], [0, -1 * (var == 1) * 2 + 1, 0], [0, 0, 1]]))  # reflect
    t3 = transforms.Affine2D().translate(val * (var == 0), val * (var == 1))  # re-translate back to original location
    return t1 + t2 + t3

def apply_transforms(ax, patches, transforms):
    """
        Apply a list of transforms to a list of patches
        :param ax: Axes on which to perform transformations
        :param patches: list of patches to transform
        :param transforms: list of matplotlib.transforms.Affine2D transforms to perform.
        :return: None
        """
    for patch in patches:
        # patch.set_transform(t1 + t2 + t3 + ax.transData)
        patch.set_transform(reduce(lambda a,b : a + b, transforms + [ax.transData]))
