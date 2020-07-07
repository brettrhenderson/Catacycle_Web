# Ouroboros Chart
# Cyclic reaction pathway figure generator - Rusty Shackleford 2018

import matplotlib
matplotlib.use('Agg')
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import math
import io
import base64
import numpy as np
import logging
import app.drawing_helpers as dh
from functools import reduce

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)

MAX_STEPS = 10

# define some default colors in case none are provided
fcolours = "#4286f4 #e2893b #de5eed #dd547d #4ee5ce #4286f4 #dd547d #4ee5ce #4286f4 #dd547d #4ee5ce".split()
rcolours = "#82abed #efb683 #edb2f4 #ef92ae #91f2e3 #82abed #ef92ae #91f2e3 #82abed #ef92ae #91f2e3".split()
incolours = fcolours

# scales the rates so they look nice in the cycle
scale = 0.5
radius = 3.0

######################################
# 1. For Drawing Cycle (Curved Arrows)
######################################
def draw_cycle(data, ax, startrange=0.15, stoprange=0.85, origin=(0,0), ext_rotation=0):
    """
    Draws the arrows for a catalytic cycle.
    :param data: a dictionary specifying the data needed to draw the cycle.
    :param ax: the axes on which to draw the cycle
    :param startrange: float. minimum arrow thickness. Default 0.15
    :param stoprange: float. maximum arrow thickness. Default 0.85
    :param origin: tuple. 2D coordinate of center of the cycle. Default (0,0)
    :param ext_rotation: Number of degrees to rotate the cycle CCW about (0,0) after drawing all arrows.
    :return: List of svg vector paths for all arrows in cycle
    """
    patches = []
    transforms = []

    # unpack data dictionary
    forward_rates = data['forward_rates'][:data['num_steps']]
    rev_rates = data['rev_rates'][:data['num_steps']]
    fcolours = data['fcolours'][:data['num_steps']]
    rcolours = data['rcolours'][:data['num_steps']]
    is_incoming = data['is_incoming'][:data['num_steps']]
    is_outgoing = data['is_outgoing'][:data['num_steps']]
    gaps = data['gaps'][:data['num_steps']]
    stretchers = try_fallback(data, 'stretchers', [1.0] * data['num_steps'])[:data['num_steps']]
    gap = float(data['gap'])
    indgap = data['indgap']
    thickness = data['multiplier']
    startrange *= thickness
    stoprange *= thickness
    scale_type = data['scale_type']
    swoop_width_scale = try_fallback(data, 'swoop_width_scale', 1.0)
    swoop_radius_scale = try_fallback(data, 'swoop_radius_scale', 1.0)
    swoop_sweep_scale = try_fallback(data, 'swoop_sweep_scale', 1.0)
    rel_head_width = try_fallback(data, 'rel_head_width', 2.0)
    rel_head_length_scaler = try_fallback(data, 'rel_head_length_scaler', 1.0)
    head_len_relative = try_fallback(data, 'head_len_rel', False)
    swoop_head_len_relative = try_fallback(data, 'swoop_head_len_rel', False)
    swoop_head_length_scaler = try_fallback(data, 'swoop_head_length_scaler', 1.0)
    swoop_start_angle_shift_multiplier = try_fallback(data, 'swoop_start_angle_shift_multiplier', 0.0)
    edgecolor_f = fcolours  # 'k' 'none'
    edgecolor_r = rcolours  # 'k' 'none'
    # edgecolor_swoops = ['none' for _ in range(len(fcolours))]
    edgecolor_swoops = fcolours
    flip = try_fallback(data, 'flip', False)
    rotation = try_fallback(data, 'rotation', 0.0)
    if not flip:
        rotation = -rotation

    # Call Sofia's Scaler function, convert rates to arrow size
    forward_rates, rev_rates, _ = scaler(forward_rates, rev_rates, startrange=startrange,
                                         stoprange=stoprange, scale_type=scale_type)

    # Splitting circle by number of forward reactions
    num_segments = len(forward_rates)
    stretchers = np.array(stretchers) / np.mean(stretchers)
    ave_delta = 360.0 / num_segments
    deltas = ave_delta * stretchers

    # transforming rates to line widths
    widths_f = [float(forward_rates[i]) * scale for i in range(num_segments)]
    widths_r = [float(rev_rates[i]) * scale for i in range(num_segments)]

    # Drawing outside and inside curves
    for i in range(0, num_segments):
        if not indgap:
            gap = dh.ensure_valid_gap(deltas[i], gap)
            # starting and ending angle for each arrow (moving counterclockwise)
            # gap/2 is added to center the gap at the top
            # make sure the gap isnt so large that the arrow length becomes 0 or negative
            theta1 = 90 - sum(deltas[:i + 1]) + (gap / 2.0)
            theta2 = 90 - (gap / 2.0) - sum(deltas[:i])
        else:
            g_1, g_0 = dh.ensure_valid_gaps(deltas[i], gaps[(i + 1) % len(gaps)], gaps[i])
            gap = (g_1 + g_0) / 2  # keep an average gap for sizing the swoops
            theta1 = 90 - sum(deltas[:i + 1]) + (g_1 / 2.0)
            theta2 = 90 - (g_0 / 2.0) - sum(deltas[:i])
        rel_head_length = (0.06 + 0.015 * num_segments) * rel_head_length_scaler
        if head_len_relative:    # arrow head length is relative to length of individual arrow
            head_length = math.radians((theta2 - theta1) * rel_head_length)
        else:
            if indgap:
                head_length = math.radians((ave_delta - sum(gaps) / len(gaps)) * rel_head_length)
            else:
                head_length = math.radians((ave_delta - gap) * rel_head_length)
        if rev_rates[i] == 0:  # draw an irreversible arrow
            f_colour = fcolours[i]
            arrow_path = dh.curved_arrow_single(theta1, theta2, radius, widths_f[i], origin=origin,
                                                rel_head_width=rel_head_width, rel_head_len=rel_head_length,
                                                abs_head_len=head_length, reverse=False)
            arrow_patch = mpatches.PathPatch(arrow_path, facecolor=f_colour, edgecolor=edgecolor_f[i])
            patches.append(arrow_patch)
        else:  # draw a reversible arrow
            f_colour = fcolours[i]
            r_colour = rcolours[i]
            f_path, r_path = dh.curved_arrow_double(theta1, theta2, radius, widths_f[i], widths_r[i], origin=origin,
                                                    rel_head_width=rel_head_width, rel_head_len=rel_head_length,
                                                    f_abs_head_len=head_length, r_abs_head_len=head_length, reverse=False)
            r_patch = mpatches.PathPatch(r_path, facecolor=r_colour, edgecolor=edgecolor_r[i])
            f_patch = mpatches.PathPatch(f_path, facecolor=f_colour, edgecolor=edgecolor_f[i])
            patches.append(r_patch)
            patches.append(f_patch)
        # input arrows/swoops
        move_center_dist = 0
        if rev_rates[i] != 0:
            move_center_dist = widths_f[i] / 2
        arrowhead_angle = math.radians(theta2 - theta1) * rel_head_length
        central_angle = math.radians(theta1 + theta2) / 2 + arrowhead_angle / 2  # shifted to be in center of tail
        swoop_width = widths_f[i] * swoop_width_scale  # may need to scale
        min_inner_rad = 0.1
        swoop_radius = max(
            [(radius - (360 / deltas[i] * 0.25) - (gap * 0.015) - (thickness * 0.1) - 0.5) * 1.5 * swoop_radius_scale,
             (swoop_width / 2 + min_inner_rad), (swoop_width / 2 + min_inner_rad) * 1.5 * swoop_radius_scale])
        ave_swoop_radius = max(
            [(radius - (num_segments * 0.25) - (gap * 0.015) - (thickness * 0.1) - 0.5) * 1.5 * swoop_radius_scale,
             (swoop_width / 2 + min_inner_rad), (swoop_width / 2 + min_inner_rad) * 1.5 * swoop_radius_scale])
        log.debug("Cycle Swoop Radius: {}".format(swoop_radius))
        swoop_sweep_angle = 180 * swoop_sweep_scale
        if swoop_head_len_relative:
            swoop_head_len = 0.3 / swoop_sweep_scale * swoop_head_length_scaler
        else:
            swoop_head_len = 0.3 / swoop_sweep_scale * swoop_head_length_scaler * ave_swoop_radius / swoop_radius
        shift = widths_f[i] / 2 - swoop_width / 2  # aligns swoop inner arc with cycle outer arc
        swoop_start_angle = math.degrees(central_angle) + 90 + (180 - swoop_sweep_angle) / 2 + (
                    swoop_sweep_angle / 2) * swoop_start_angle_shift_multiplier
        swoop_end_angle = math.degrees(central_angle) + 270 - (180 - swoop_sweep_angle) / 2 + (
                    swoop_sweep_angle / 2) * swoop_start_angle_shift_multiplier
        dist_to_swoop_center = radius + shift + swoop_radius + move_center_dist
        swoop_origin = (origin[0] + dist_to_swoop_center * math.cos(central_angle),
                        origin[1] + dist_to_swoop_center * math.sin(central_angle))

        if is_incoming[i] and is_outgoing[i]:
            swoop_path = dh.curved_arrow_single(swoop_start_angle, swoop_end_angle, swoop_radius, swoop_width,
                                                origin=swoop_origin, rel_head_width=rel_head_width,
                                                rel_head_len=swoop_head_len, abs_head_len=swoop_head_len, reverse=True)
            swoop_patch = mpatches.PathPatch(swoop_path, facecolor=f_colour, edgecolor=edgecolor_swoops[i])
            patches.append(swoop_patch)

        elif is_outgoing[i]:
            swoop_path = dh.curved_arrow_single(math.degrees(central_angle) + 180, swoop_end_angle, swoop_radius,
                                                swoop_width, origin=swoop_origin, rel_head_width=rel_head_width,
                                                rel_head_len=swoop_head_len, abs_head_len=swoop_head_len, reverse=True)
            swoop_patch = mpatches.PathPatch(swoop_path, facecolor=f_colour, edgecolor=edgecolor_swoops[i])
            patches.append(swoop_patch)

        elif is_incoming[i]:
            swoop_path = dh.filled_circular_arc(swoop_start_angle, math.degrees(central_angle) + 180, swoop_radius,
                                                swoop_width, origin=swoop_origin)
            swoop_patch = mpatches.PathPatch(swoop_path, facecolor=f_colour, edgecolor=edgecolor_swoops[i])
            patches.append(swoop_patch)

    if flip:
        transforms.append(dh.get_reflect_trans(0, origin[0]))
    if rotation:
        transforms.append(dh.get_rotate_trans(rotation, origin))
    if ext_rotation:
        # rotate about (0,0), not the cycle origin
        transforms.append(dh.get_rotate_trans(ext_rotation, (0, 0)))

    dh.apply_transforms(ax, patches, transforms)
    for patch in patches:
        ax.add_patch(patch)
    if len(transforms):
        return [mpath.Path.transformed(patch.get_path(), reduce(lambda a, b: a + b, transforms)) for patch in patches]
    else:
        return [patch.get_path() for patch in patches]


def draw(data=None, startrange=0.15, stoprange=0.85, f_format='svg', figsize=(8, 8), return_image=False):
    # set defaults and declare variables
    img = io.BytesIO()    # file-like object to hold image

    # Figure initialization
    fig = plt.figure(1, figsize=figsize)
    ax = fig.add_subplot(111, autoscale_on=False) #, xlim=(-6.5, 6.5), ylim=(-6.5, 6.5))
    plt.axis('off')

    if data['plot1']:
        if data['is_vert']:
            paths1 = draw_cycle(data['data1'], ax, startrange, stoprange, origin=(2 * radius * data['trans1'], 0),
                                ext_rotation=-np.pi/2)
        else:
            paths1 = draw_cycle(data['data1'], ax, startrange, stoprange, origin=(2 * radius * data['trans1'], 0))
    else:
        paths1 = []
    if data['plot2']:
        if data['is_vert']:
            paths2 = draw_cycle(data['data2'], ax, startrange, stoprange,
                                origin=(2 * radius*data['trans2'] + 2 * radius, 0), ext_rotation=-np.pi/2)
        else:
            paths2 = draw_cycle(data['data2'], ax, startrange, stoprange,
                                origin=(2 * radius*data['trans2'] + 2 * radius, 0))
    else:
        paths2 = []
    paths = paths1 + paths2
    if len(paths):
        dh.set_ax_lims(ax, paths1 + paths2)
    # ax.invert_xaxis()
    plt.draw()

    # correct mimetype based on filetype (for displaying in browser)
    if f_format == 'svg':
        mimetype = 'image/svg+xml'
    elif f_format == 'png':
        mimetype = 'image/png'
    elif f_format == 'jpg':
        mimetype = 'image/jpg'
    elif f_format == 'pdf':
        mimetype = 'application/pdf'
    elif f_format == 'eps':
        mimetype = 'application/postscript'
    else:
        raise ValueError('Image format {} not supported.'.format(format))

    plt.savefig(img, format=f_format, transparent=True)
    plt.close()
    img.seek(0)
    if not return_image:
        graph_url = base64.b64encode(img.getvalue()).decode()
        return 'data:{};base64,{}'.format(mimetype, graph_url)
    else:
        return img, mimetype


###################################################
# 2. For Drawing Straight Arrows for Side Reactions
###################################################

def draw_straight(data, startrange=0.15, stoprange=0.85, f_format='svg', figsize=(8, 8), return_image=False):

    if data['p1_active']:
        data = data['data1']
    else:
        data = data['data2']

    # keep track of all paths to set the bounds of the canvas
    paths = []

    # set defaults and declare variables
    img = io.BytesIO()    # file-like object to hold image

    # data is passed in as a python dictionary (which is collected from a web form)
    forward_rates = data['forward_rates'][:data['num_steps']]
    rev_rates = data['rev_rates'][:data['num_steps']]
    rev_rate = data['r_rate_straight']
    for_rate = data['f_rate_straight']
    forward_rates.append(for_rate)
    rev_rates.append(rev_rate)
    gaps = data['gaps'][:data['num_steps']]
    gap = float(data['gap'])
    indgap = data['indgap']
    fcolour = data['f_color_straight']
    rcolour = data['r_color_straight']
    is_incoming = data['incoming_straight']
    is_outgoing = data['outgoing_straight']
    thickness = data['multiplier']
    startrange *= thickness
    stoprange *= thickness
    scale_type = data['scale_type']
    swoop_width_scale = try_fallback(data, 'swoop_width_scale', 1.0)
    swoop_radius_scale = try_fallback(data, 'swoop_radius_scale', 1.0)
    swoop_sweep_scale = try_fallback(data, 'swoop_sweep_scale', 1.0)
    rel_head_width = try_fallback(data, 'rel_head_width', 2.0)
    rel_head_length_scaler = try_fallback(data, 'rel_head_length_scaler', 1.0)
    swoop_head_length_scaler = try_fallback(data, 'swoop_head_length_scaler', 1.0)
    swoop_start_angle_shift_multiplier = try_fallback(data, 'swoop_start_angle_shift_multiplier', 0.0)
    edgecolor_f = fcolour  # 'k' #'none'
    edgecolor_r = rcolour  # 'k' #'none'
    edgecolor_swoop = fcolour    # 'none'
    flip = try_fallback(data, 'flip', False)

    # Splitting circle by number of forward reactions
    num_segments = len(forward_rates) - 1
    delta = 360.0 / num_segments

    # calculate the length of a segment and use the same length for a straight line to preserve scaling
    if not indgap:
        gap = dh.ensure_valid_gap(delta, gap)
    else:
        gaps = dh.ensure_all_valid_gaps(delta, gaps)
        gap = sum(gaps) / len(gaps)  # keep an average gap for sizing the swoops
    theta1 = 90 - delta + (gap / 2.0)
    theta2 = 90 - (gap / 2.0)

    length = math.radians(theta2 - theta1) * radius
    rel_head_length = (0.06 + 0.015 * num_segments) * rel_head_length_scaler


    # Call Sofia's Scaler function, convert rates to arrow size
    forward_rates, rev_rates, _ = scaler(forward_rates, rev_rates, startrange=startrange,
                                         stoprange=stoprange, scale_type=scale_type)

    # we only need the scaled rates for the straight arrow rxn
    f_rate_scaled, r_rate_scaled = forward_rates[-1], rev_rates[-1]

    f_width, r_width = scale * f_rate_scaled, scale * r_rate_scaled


    # Figure initialization
    fig = plt.figure(1, figsize=figsize)
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 5), ylim=(-5, 5))
    plt.axis('off')

    # add arrows to the axes
    if rev_rate == 0:  # draw an irreversible arrow
        arrow_path = dh.straight_arrow_single(length, f_width, origin=(0, 0),
                                              rel_head_width=rel_head_width, rel_head_len=rel_head_length,
                                              abs_head_len=None, reverse=False)
        paths.append(arrow_path)
        arrow_patch = mpatches.PathPatch(arrow_path, facecolor=fcolour, edgecolor=edgecolor_f)
        ax.add_patch(arrow_patch)
    else:  # draw a reversible arrow
        f_path, r_path = dh.straight_arrow_double(length, f_width, r_width, origin=(0,0), rel_head_width=rel_head_width,
                                                f_abs_head_len=None, r_abs_head_len=None, rel_head_len=rel_head_length,
                                                reverse=False)
        paths += [f_path, r_path]
        r_patch = mpatches.PathPatch(r_path, facecolor=rcolour, edgecolor=edgecolor_r)
        f_patch = mpatches.PathPatch(f_path, facecolor=fcolour, edgecolor=edgecolor_f)
        ax.add_patch(r_patch)
        ax.add_patch(f_patch)

    # input arrows/swoops
    move_center_y = 0
    if rev_rate != 0:
        move_center_y = f_width / 2
    swoop_width = f_width * swoop_width_scale
    min_inner_rad = 0.1
    swoop_radius = max([(radius - (num_segments * 0.25) - (gap * 0.015) - (thickness * 0.1) - 0.5) * 1.5 * swoop_radius_scale,
                        (swoop_width / 2 + min_inner_rad), (swoop_width / 2 + min_inner_rad) * 1.5 * swoop_radius_scale])
    log.debug("Straight Swoop Radius: {}".format(swoop_radius))
    swoop_sweep_angle = 180 * swoop_sweep_scale
    swoop_head_len = 0.3 / swoop_sweep_scale * swoop_head_length_scaler
    shift = f_width / 2 - swoop_width / 2  # aligns swoop inner arc with cycle outer arc
    swoop_start_angle = 180 + (180 - swoop_sweep_angle) / 2 + (swoop_sweep_angle / 2) * swoop_start_angle_shift_multiplier
    swoop_end_angle = 360 - (180 - swoop_sweep_angle) / 2 + (swoop_sweep_angle / 2) * swoop_start_angle_shift_multiplier
    swoop_origin = (-rel_head_length * length / 2, shift + swoop_radius + move_center_y)

    if is_incoming and is_outgoing:
        swoop_path = dh.curved_arrow_single(swoop_start_angle, swoop_end_angle, swoop_radius, swoop_width,
                                            origin=swoop_origin, rel_head_width=rel_head_width,
                                            rel_head_len=swoop_head_len, abs_head_len=swoop_head_len, reverse=True)
        paths.append(swoop_path)
        swoop_patch = mpatches.PathPatch(swoop_path, facecolor=fcolour, edgecolor=edgecolor_swoop)
        ax.add_patch(swoop_patch)

    elif is_outgoing:
        swoop_path = dh.curved_arrow_single(270, swoop_end_angle, swoop_radius,
                                            swoop_width, origin=swoop_origin, rel_head_width=rel_head_width,
                                            rel_head_len=swoop_head_len, abs_head_len=swoop_head_len, reverse=True)
        paths.append(swoop_path)
        swoop_patch = mpatches.PathPatch(swoop_path, facecolor=fcolour, edgecolor=edgecolor_swoop)
        ax.add_patch(swoop_patch)

    elif is_incoming:
        swoop_path = dh.filled_circular_arc(swoop_start_angle, 270, swoop_radius,
                                            swoop_width, origin=swoop_origin)
        paths.append(swoop_path)
        swoop_patch = mpatches.PathPatch(swoop_path, facecolor=fcolour, edgecolor=edgecolor_swoop)
        ax.add_patch(swoop_patch)

    dh.set_ax_lims(ax, paths)
    # if flip:
    #     ax.invert_xaxis()
    # draw on the axes
    plt.draw()

    # correct mimetype based on filetype (for displaying in browser)
    if f_format == 'svg':
        mimetype = 'image/svg+xml'
    elif f_format == 'png':
        mimetype = 'image/png'
    elif f_format == 'jpg':
        mimetype = 'image/jpg'
    elif f_format == 'pdf':
        mimetype = 'application/pdf'
    elif f_format == 'eps':
        mimetype = 'application/postscript'
    else:
        raise ValueError('Image format {} not supported.'.format(format))

    # save the figure to the temporary file-like object
    plt.savefig(img, format=f_format, transparent=True)
    plt.close()
    img.seek(0)
    if not return_image:
        graph_url = base64.b64encode(img.getvalue()).decode()
        return 'data:{};base64,{}'.format(mimetype, graph_url)
    else:
        return img, mimetype


########################################################################################################
########################################################################################################


def scaler(forward_rates, rev_rates, startrange=0.1, stoprange=0.8, scale_type='Linear'):
    """
    Transforming rates to be within specified range defined by startrange and stoprange:

    Can use linear or logarithmic scale, which is preserved when transforming the data.
    :param forward_rates: a list of forward rates as floats or ints
    :param rev_rates: a list of reverse rates as floats or ints
    :param startrange: float, first number of the range you want output to take
    :param stoprange: float, last number of range for output to take
    :param scale_type: 'Linear', 'Logarithmic', or 'Preserve Multiples'.
    :return: (forward_rates, rev_rates), a tuple of the original lists scaled properly
    """

    if scale_type not in ['Linear', 'Logarithmic', 'Preserve Multiples']:
        raise ValueError("scale_type must be Linear, Logarithmic, or Preserve Multiples")

    forward_rates = np.array(forward_rates).astype(np.float)
    rev_rates = np.array(rev_rates).astype(np.float)

    log.debug("original forward: {}".format(forward_rates))
    log.debug("original reverse: {}".format(rev_rates))

    # make sure to only scale based on the non-zero elements.  Zeros will not affect scaling
    f_nonzero = np.nonzero(forward_rates)
    r_nonzero = np.nonzero(rev_rates)

    # scale logarithmically and then apply the transformation to be within specified bounds (leave zeros)
    if scale_type == 'Logarithmic':
        log.debug("logarithmic scale selected")
        forward_rates[f_nonzero] = np.log10(forward_rates[f_nonzero])
        rev_rates[r_nonzero] = np.log10(rev_rates[r_nonzero])
        log.debug("post-log forward: {}".format(forward_rates))
        log.debug("post-log reverse: {}".format(rev_rates))

    f_min = np.min(forward_rates[f_nonzero])
    f_max = forward_rates.max()
    r_max = rev_rates.max()
    if not any(rev_rates):
        r_min = f_min
    else:
        r_min = np.min(rev_rates[r_nonzero])

    maxima = max(f_max, r_max)
    minima = min(f_min, r_min)

    ranger = stoprange - startrange

    if minima == maxima:
        if scale_type == 'Preserve Multiples':
            # forward_rates[f_nonzero] = stoprange / 2.0
            # rev_rates[r_nonzero] = stoprange / 2.0
            increments = ranger / 5  # for simple scaling only
            log.debug("Increment: {}".format(increments))
            forward_rates = increments * forward_rates
            rev_rates = increments * rev_rates
        else:
            # if all rates are the same, just set them to be a medium value in the desired range
            forward_rates[f_nonzero] = np.mean([stoprange, startrange])
            rev_rates[r_nonzero] = np.mean([stoprange, startrange])
    else:
        if scale_type == 'Preserve Multiples':
            # forward_rates = forward_rates / maxima * stoprange
            # rev_rates = rev_rates / maxima * stoprange
            increments = ranger / 5    # for simple scaling only
            log.debug("Increment: {}".format(increments))
            forward_rates = increments * forward_rates
            rev_rates = increments * rev_rates
        else:
            log.debug("Max != Min")
            # otherwise, scale and move the rates to be between the desired endpoints
            forward_rates[f_nonzero] = ((forward_rates[f_nonzero] - minima) / (maxima - minima) * ranger + startrange)
            rev_rates[r_nonzero] = ((rev_rates[r_nonzero] - minima) / (maxima - minima) * ranger + startrange)
    forward_rates = forward_rates.tolist()
    rev_rates = rev_rates.tolist()

    log.debug("final forward: {}".format(forward_rates))
    log.debug("final reverse: {}".format(rev_rates))

    return forward_rates, rev_rates, maxima - minima

def try_fallback(dictionary, key, fb):
    try:
        return dictionary[key]
    except KeyError:
        return fb
