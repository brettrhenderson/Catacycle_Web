# Ouroboros Chart
# Cyclic reaction pathway figure generator - Rusty Shackleford 2018
# Set up for a 8x8 inch figure
# Still needs scale for real kinetic data. Transform to 0.1 to 1 for clean image.

import matplotlib
matplotlib.use('Agg')
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import math
import random
import io
import base64
import numpy as np
import logging
import app.drawing_helpers as dh

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)

MAX_STEPS = 10

# define some default colors in case none are provided
fcolours = "#4286f4 #e2893b #de5eed #dd547d #4ee5ce #4286f4 #dd547d #4ee5ce #4286f4 #dd547d #4ee5ce".split()
rcolours = "#82abed #efb683 #edb2f4 #ef92ae #91f2e3 #82abed #ef92ae #91f2e3 #82abed #ef92ae #91f2e3".split()
incolours = fcolours

# scales the rates so they look nice in the cycle
scale = 0.8
radius = 3.0

######################################
# 1. For Drawing Cycle (Curved Arrows)
######################################
def draw(data=None, startrange=0.15, stoprange=0.85, f_format='svg', figsize=(8, 8)):

    # set defaults and declare variables
    img = io.BytesIO()    # file-like object to hold image

    # unpack data dictionary
    forward_rates = data['forward_rates'][:data['num_steps']]
    rev_rates = data['rev_rates'][:data['num_steps']]
    fcolours = data['fcolours'][:data['num_steps']]
    rcolours = data['rcolours'][:data['num_steps']]
    incolours = fcolours
    is_incoming = data['is_incoming'][:data['num_steps']]
    is_outgoing = data['is_outgoing'][:data['num_steps']]
    gap = float(data['gap'])
    startrange *= data['multiplier']
    stoprange *= data['multiplier']
    scale_type = data['scale_type']
    f_format = data['f_format'].split('.')[1]
    swoop_width_scale = 1.0
    swoop_radius_scale = 1.0
    swoop_sweep_scale = 0.9
    edgecolor = 'none'
    rel_head_width = 0.5
    rel_head_length_scaler = 1.0
    swoop_head_length_scaler = 1.0



    # Call Sofia's Scaler function, convert rates to arrow size
    forward_rates, rev_rates, _ = scaler(forward_rates, rev_rates, startrange=startrange,
                                         stoprange=stoprange, scale_type=scale_type)

    # Figure initialization
    fig = plt.figure(1, figsize=figsize)
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 5), ylim=(-5, 5))
    plt.axis('off')

    # Splitting circle by number of forward reactions
    num_segments = len(forward_rates)
    delta = 360.0/num_segments

    # transforming rates to line widths
    widths_f = [float(forward_rates[i]) * scale for i in range(num_segments)]
    widths_r = [float(rev_rates[i]) * scale for i in range(num_segments)]

    # Drawing outside and inside curves
    for i in range(0, num_segments):

        # starting and ending angle for each arrow (moving counterclockwise)
        # gap/2 is added to center the gap at the top
        theta1 = 90 - delta * (i + 1) + (gap / 2.0)
        theta2 = 90 - (gap / 2.0) - delta * i
        rel_head_length = (0.1 + 0.015 * num_segments) * rel_head_length_scaler
        print('Cycle: {}'.format(rel_head_length))

        if rev_rates[i] == 0:    # draw an irreversible arrow
            f_colour = fcolours[i]
            arrow_path = dh.curved_arrow_single(theta1, theta2, radius, widths_f[i], origin=(0,0),
                                                rel_head_width=rel_head_width, rel_head_len=rel_head_length,
                                                abs_head_len=None, reverse=False)
            arrow_patch = mpatches.PathPatch(arrow_path, facecolor=f_colour, edgecolor=edgecolor)
            ax.add_patch(arrow_patch)
        else:    # draw a reversible arrow
            f_colour = fcolours[i]
            r_colour = rcolours[i]
            f_path, r_path = dh.curved_arrow_double(theta1, theta2, radius, widths_f[i], widths_r[i], origin=(0, 0),
                                                    rel_head_width=rel_head_width, rel_head_len=rel_head_length,
                                                    f_abs_head_len=None, r_abs_head_len=None, reverse=False)
            f_patch = mpatches.PathPatch(f_path, facecolor=f_colour, edgecolor=edgecolor)
            r_patch = mpatches.PathPatch(r_path, facecolor=r_colour, edgecolor=edgecolor)
            ax.add_patch(f_patch)
            ax.add_patch(r_patch)

        # input arrows/swoops
        arrowhead_angle = math.radians(theta2 - theta1) * rel_head_length
        central_angle = math.radians(theta1 + theta2) / 2 + arrowhead_angle / 2  # shifted to be in center of tail
        swoop_width = widths_f[i] * swoop_width_scale  # may need to scale
        swoop_radius = radius / (num_segments / 2) * swoop_radius_scale
        swoop_sweep_angle = 180 * swoop_sweep_scale
        swoop_head_len = 0.3 / swoop_sweep_scale * swoop_head_length_scaler
        shift = widths_f[i] / 2 - swoop_width / 2    # aligns swoop inner arc with cycle outer arc
        swoop_start_angle = math.degrees(central_angle) + 90 + (180 - swoop_sweep_angle) / 2 + math.degrees(swoop_head_len) / 2
        swoop_end_angle = math.degrees(central_angle) + 270 - (180 - swoop_sweep_angle) / 2 + math.degrees(swoop_head_len) / 2
        dist_to_swoop_center = radius + shift + swoop_radius
        swoop_origin = (dist_to_swoop_center * math.cos(central_angle), dist_to_swoop_center * math.sin(central_angle))

        if is_incoming[i] and is_outgoing[i]:
            swoop_path = dh.curved_arrow_single(swoop_start_angle, swoop_end_angle, swoop_radius, swoop_width,
                                                origin=swoop_origin, rel_head_width=rel_head_width,
                                                rel_head_len=swoop_head_len, abs_head_len=swoop_head_len, reverse=True)
            swoop_patch = mpatches.PathPatch(swoop_path, facecolor=f_colour, edgecolor=edgecolor)
            ax.add_patch(swoop_patch)

        elif is_outgoing[i]:
            swoop_path = dh.curved_arrow_single(math.degrees(central_angle) + 180, swoop_end_angle, swoop_radius,
                                                swoop_width, origin=swoop_origin, rel_head_width=rel_head_width,
                                                rel_head_len=swoop_head_len, abs_head_len=swoop_head_len, reverse=True)
            swoop_patch = mpatches.PathPatch(swoop_path, facecolor=f_colour, edgecolor=edgecolor)
            ax.add_patch(swoop_patch)

        elif is_incoming[i]:
            swoop_path = dh.filled_circular_arc(swoop_start_angle, math.degrees(central_angle) + 180, swoop_radius,
                                                swoop_width, origin=swoop_origin)
            swoop_patch = mpatches.PathPatch(swoop_path, facecolor=f_colour, edgecolor=edgecolor)
            ax.add_patch(swoop_patch)
    plt.draw()

    # correct mimetype based on filetype (for displaying in browser)
    if f_format == 'svg':
        mimetype = 'image/svg+xml'
    elif f_format == 'png':
        mimetype = 'image/png'
    else:
        raise ValueError('Image format {} not supported.'.format(format))

    plt.savefig(img, format=f_format, transparent=True)
    plt.close()
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return 'data:{};base64,{}'.format(mimetype, graph_url)


###################################################
# 2. For Drawing Straight Arrows for Side Reactions
###################################################

def draw_straight(data, startrange=0.1, stoprange=0.8, f_format='svg', figsize=(8, 8)):

    # set defaults and declare variables
    img = io.BytesIO()    # file-like object to hold image

    # data is passed in as a python dictionary (which is collected from a web form)
    forward_rates = data['forward_rates'][:data['num_steps']]
    rev_rates = data['rev_rates'][:data['num_steps']]
    rev_rate = data['r_rate_straight']
    for_rate = data['f_rate_straight']
    forward_rates.append(for_rate)
    rev_rates.append(rev_rate)
    gap = float(data['gap'])
    fcolour = data['f_color_straight']
    rcolour = data['r_color_straight']
    is_incoming = data['incoming_straight']
    is_outgoing = data['outgoing_straight']
    startrange *= data['multiplier']
    stoprange *= data['multiplier']
    scale_type = data['scale_type']
    f_format = data['f_format'].split('.')[1]
    swoop_width_scale = 1.0
    swoop_radius_scale = 1.0
    swoop_sweep_scale = 1.0
    edgecolor = 'none'
    rel_head_width = 0.5
    rel_head_length_scaler = 1.0
    swoop_head_length_scaler = 1.0

    # Splitting circle by number of forward reactions
    num_segments = len(forward_rates) - 1
    delta = 360.0 / num_segments

    # calculate the length of a segment and use the same length for a straight line to preserve scaling
    theta1 = 90 - delta + (gap / 2.0)
    theta2 = 90 - (gap / 2.0)

    length = math.radians(theta2 - theta1) * radius
    rel_head_length = (0.1 + 0.015 * num_segments) * rel_head_length_scaler


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
        arrow_patch = mpatches.PathPatch(arrow_path, facecolor=fcolour, edgecolor=edgecolor)
        ax.add_patch(arrow_patch)
    else:  # draw a reversible arrow
        f_path, r_path = dh.straight_arrow_double(length, f_width, r_width, origin=(0,0), rel_head_width=rel_head_width,
                                                f_abs_head_len=None, r_abs_head_len=None, rel_head_len=rel_head_length,
                                                reverse=False)
        f_patch = mpatches.PathPatch(f_path, facecolor=fcolour, edgecolor=edgecolor)
        r_patch = mpatches.PathPatch(r_path, facecolor=rcolour, edgecolor=edgecolor)
        ax.add_patch(f_patch)
        ax.add_patch(r_patch)

    # input arrows/swoops
    move_center = np.array([-rel_head_length * length / 2, 0])  # shift to account for arrowhead
    swoop_width = f_width * swoop_width_scale
    swoop_radius = radius / (num_segments / 2) * swoop_radius_scale
    swoop_sweep_angle = 180 * swoop_sweep_scale
    swoop_head_len = 0.3 / swoop_sweep_scale * swoop_head_length_scaler
    shift = f_width / 2 - swoop_width / 2  # aligns swoop inner arc with cycle outer arc
    swoop_start_angle = 180 + (180 - swoop_sweep_angle) / 2 + math.degrees(swoop_head_len) / 6
    swoop_end_angle = 360 - (180 - swoop_sweep_angle) / 2 + math.degrees(swoop_head_len) / 6
    swoop_origin = (-rel_head_length * length / 2, shift + swoop_radius)

    if is_incoming and is_outgoing:
        swoop_path = dh.curved_arrow_single(swoop_start_angle, swoop_end_angle, swoop_radius, swoop_width,
                                            origin=swoop_origin, rel_head_width=rel_head_width,
                                            rel_head_len=swoop_head_len, abs_head_len=swoop_head_len, reverse=True)
        swoop_patch = mpatches.PathPatch(swoop_path, facecolor=fcolour, edgecolor=edgecolor)
        ax.add_patch(swoop_patch)

    elif is_outgoing:
        swoop_path = dh.curved_arrow_single(270, swoop_end_angle, swoop_radius,
                                            swoop_width, origin=swoop_origin, rel_head_width=rel_head_width,
                                            rel_head_len=swoop_head_len, abs_head_len=swoop_head_len, reverse=True)
        swoop_patch = mpatches.PathPatch(swoop_path, facecolor=fcolour, edgecolor=edgecolor)
        ax.add_patch(swoop_patch)

    elif is_incoming:
        swoop_path = dh.filled_circular_arc(swoop_start_angle, 270, swoop_radius,
                                            swoop_width, origin=swoop_origin)
        swoop_patch = mpatches.PathPatch(swoop_path, facecolor=fcolour, edgecolor=edgecolor)
        ax.add_patch(swoop_patch)

    # draw on the axes
    plt.draw()

    # correct mimetype based on filetype (for displaying in browser)
    if f_format == 'svg':
        mimetype = 'image/svg+xml'
    elif f_format == 'png':
        mimetype = 'image/png'
    else:
        raise ValueError('Image format {} not supported.'.format(format))

    # save the figure to the temporary file-like object
    plt.savefig(img, format=f_format, transparent=True)
    plt.close()
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return 'data:{};base64,{}'.format(mimetype, graph_url)


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
        forward_rates[f_nonzero]=np.log10(forward_rates[f_nonzero])
        rev_rates[r_nonzero]=np.log10(rev_rates[r_nonzero])
        log.debug("post-log forward: {}".format(forward_rates))
        log.debug("post-log reverse: {}".format(rev_rates))

    f_min = np.min(forward_rates[f_nonzero])
    f_max = forward_rates.max()
    r_max = rev_rates.max()
    if r_max == 0:
        r_min = f_min
    else:
        r_min = np.min(rev_rates[r_nonzero])

    log.debug('f_min, f_max: {}'.format((f_min, f_max)))
    log.debug('r_min, r_max: {}'.format((r_min, r_max)))

    maxima = max(f_max, r_max)
    minima = min(f_min, r_min)

    ranger = stoprange - startrange

    # incase k range = 0
    if minima == maxima:
        if scale_type == 'Preserve Multiples':
            forward_rates[f_nonzero] = stoprange / 2.0
            rev_rates[r_nonzero] = stoprange / 2.0
        else:
            # if all rates are the same, just set them to be a medium value in the desired range
            forward_rates[f_nonzero] = np.mean([stoprange, startrange])
            rev_rates[r_nonzero] = np.mean([stoprange, startrange])
    else:
        if scale_type == 'Preserve Multiples':
            forward_rates = forward_rates / maxima * stoprange
            rev_rates = rev_rates / maxima * stoprange
        else:
            # otherwise, scale and move the rates to be between the desired endpoints
            forward_rates[f_nonzero] = ((forward_rates[f_nonzero] - minima) / (maxima - minima) * ranger + startrange)
            rev_rates[r_nonzero] = ((rev_rates[r_nonzero] - minima) / (maxima - minima) * ranger + startrange)
    forward_rates = forward_rates.tolist()
    rev_rates = rev_rates.tolist()

    log.debug("final forward: {}".format(forward_rates))
    log.debug("final reverse: {}".format(rev_rates))

    return forward_rates, rev_rates, maxima - minima
