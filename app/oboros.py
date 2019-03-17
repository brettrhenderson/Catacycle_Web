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

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)

MAX_STEPS = 10

def draw(data=None, startrange=0.1, stoprange=0.8, f_format='svg'):

    # set defaults and declare variables
    img = io.BytesIO()    # file-like object to hold image

    fcolours = "#4286f4 #e2893b #de5eed #dd547d #4ee5ce #4286f4 #dd547d #4ee5ce #4286f4 #dd547d #4ee5ce".split()
    rcolours = "#82abed #efb683 #edb2f4 #ef92ae #91f2e3 #82abed #ef92ae #91f2e3 #82abed #ef92ae #91f2e3".split()
    incolours = fcolours

    swoops = []
    forward_rates = []
    rev_rates = []
    is_incoming = [False for i in range(MAX_STEPS)]   # no incoming swoops by default
    is_outgoing = [False for i in range(MAX_STEPS)]  # no outgoing swoops by default

    scale_type = 'Logarithmic'
    gap = 5  # default gap without settings
    scale = 23.9   # will scale pending on image size -- connects graph space to figure space


    # Read in the data from its source
    if data is None:    # when data is provided via a csv file
        data = open("data.dat", 'r')
        for line in data:
            if "f_rate" in line:
                forward_rates.append(line.split()[2])
            if "r_rate" in line:
                rev_rates.append(line.split()[2])
            if "gap" in line:
                gap = float(line.split()[2])

    else:    # when data is passed in as a python dictionary (as when it is collected from a web form)
        forward_rates = data['forward_rates'][:data['num_steps']]
        rev_rates = data['rev_rates'][:data['num_steps']]
        fcolours = data['fcolours'][:data['num_steps']]
        rcolours = data['rcolours'][:data['num_steps']]
        incolours = fcolours
        is_incoming = data['is_incoming'][:data['num_steps']]
        is_outgoing = data['is_outgoing'][:data['num_steps']]
        gap = float(data['gap'])
        multiplier = data['multiplier']
        startrange *= multiplier
        stoprange *= multiplier
        scale_type = data['scale_type']
        f_format = data['f_format'].split('.')[1]



    # Call Sofia's Scaler function, convert rates to arrow size
    forward_rates, rev_rates, range_rates = scaler(forward_rates, rev_rates, startrange=startrange,
                                                   stoprange=stoprange, scale_type=scale_type)

    # Figure initialization
    fig = plt.figure(1, figsize=(8, 8))
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 5), ylim=(-5, 5))
    plt.axis('off')

    # Splitting circle by number of forward reactions
    num_segments = len(forward_rates)
    delta = 360.0/num_segments

    # Coordinates for curves
    transformed_rates_r = []
    transformed_rates_f = []
    radial_offsets_f = []
    radial_offsets_r = []



    # transforming rates to line widths
    for i in range(0, num_segments):
        if rev_rates[i] == 0:
            forward_rates[i] /= 2

        log.debug('corrected forward rate {}: {}'.format(i+1, forward_rates[i]))
        radial_offsets_f.append(float(forward_rates[i])/2)
        radial_offsets_r.append(float(rev_rates[i])/2)
        transformed_rates_f.append(float(forward_rates[i])*scale)
        transformed_rates_r.append(float(rev_rates[i])*scale)


    # Drawing outside and inside curves
    for i in range(0,num_segments):

        # starting and ending angle for each arrow
        theta1 = 90-delta*i
        theta2 = 90-gap-delta*(i-1)

        # Outside Arrows / forward rates
        if fcolours[i] == "blank" or fcolours[i] is None:    # Assign a random color if none is provided
            r = lambda: random.randint(0,255)
            col = ('#%02X%02X%02X' % (r(),r(),r()))
        else:
            col = fcolours[i]
        Curve = mpatches.Arc((0,0),height=6+radial_offsets_f[i],width=6+radial_offsets_f[i],angle=1,
                             theta1=theta1,theta2=theta2,linewidth=transformed_rates_f[i],color=col)
        ax.add_patch(Curve)
        col = rcolours[i]
        Curve = mpatches.Arc((0,0),height=6-radial_offsets_r[i],width=6-radial_offsets_r[i],angle=1,theta1=theta1,
                             theta2=theta2,linewidth=transformed_rates_r[i],color=col)
        ax.add_patch(Curve)
        a_angle = ((90-delta*(i))*(math.pi/180.0))+((+2)*(math.pi/180.0))/2	 # Starting point angle for outside triangles
        b_angle = ((90-delta*(i-1))*(math.pi/180.0))+((gap-(3*gap-(2)))*(math.pi/180.0))/2	 # Starting point angle for inside triangles
        col = fcolours[i]

        f_angle_offset =10*float(forward_rates[i])*math.pi/180.0
        r_angle_offset =10*float(rev_rates[i])*math.pi/180.0

        # Outside Arrows
        a_x = 3*math.cos(a_angle)
        a_y = 3*math.sin(a_angle)
        b_vec = (3+(float(forward_rates[i])))
        c_vec = (3+(float(forward_rates[i])))

        b_x = (b_vec*math.cos(a_angle))
        b_y = (b_vec*math.sin(a_angle))
        c_x = (b_vec*math.cos(a_angle+0.1+f_angle_offset))
        c_y = (b_vec*math.sin(a_angle+0.1+f_angle_offset))
        d_x =(3+float(forward_rates[i])/2)*math.cos(a_angle+0.1+f_angle_offset)
        d_y =(3+float(forward_rates[i])/2)*math.sin(a_angle+0.1+f_angle_offset)
        e_x = (c_vec*math.cos(a_angle+0.1+f_angle_offset))
        e_y =(c_vec*math.sin(a_angle+0.1+f_angle_offset))
        tri1 = plt.Polygon(((a_x,a_y),(b_x,b_y),(c_x,c_y)),color='w')
        tri2 = plt.Polygon(((a_x,a_y),(d_x,d_y),(e_x,e_y)),color=col)
        ax.add_patch(tri1)
        ax.add_patch(tri2)

        # Inside Arrows / reverse rates
        if rev_rates[i] != 0:    # if reverse rate is 0, make forward arrowhead symmetrical
            col = rcolours[i]
            ai_x = 3*math.cos(b_angle)
            ai_y = 3*math.sin(b_angle)
            bi_vec = (3-(float(rev_rates[i])))
            ci_vec = (3-(float(rev_rates[i])+(float(rev_rates[i])/4)))
            ci_vec = (3-(float(rev_rates[i])))
            bi_x = (bi_vec*math.cos(b_angle))
            bi_y = (bi_vec*math.sin(b_angle))
            ci_x = (bi_vec*math.cos(b_angle-0.1-r_angle_offset))
            ci_y = (bi_vec*math.sin(b_angle-0.1-r_angle_offset))

            di_x =(3-float(rev_rates[i])/2)*math.cos(b_angle-0.1-r_angle_offset)
            di_y =(3-float(rev_rates[i])/2)*math.sin(b_angle-0.1-r_angle_offset)
            ei_x = (ci_vec*math.cos(b_angle-0.1-r_angle_offset))
            ei_y =(ci_vec*math.sin(b_angle-0.1-r_angle_offset))
            tri3 = plt.Polygon(((ai_x,ai_y),(bi_x,bi_y),(ci_x,ci_y)),color='w')
            tri4 = plt.Polygon(((ai_x,ai_y),(di_x,di_y),(ei_x,ei_y)),color=col)
            ax.add_patch(tri3)
            ax.add_patch(tri4)

        if rev_rates[i] == 0.0:

            col = fcolours[i]
            Curve = mpatches.Arc((0,0),height=6-radial_offsets_f[i],width=6-radial_offsets_f[i],angle=1,
                                 theta1=theta1,theta2=theta2,linewidth=transformed_rates_f[i],color=col)
            ax.add_patch(Curve)
            a_x = 3*math.cos(a_angle)
            a_y = 3*math.sin(a_angle)
            b_vec = (3-(float(forward_rates[i])))
            c_vec = (3-(float(forward_rates[i])))

            b_x = (b_vec*math.cos(a_angle))
            b_y = (b_vec*math.sin(a_angle))
            c_x = (b_vec*math.cos(a_angle+0.1+f_angle_offset))
            c_y = (b_vec*math.sin(a_angle+0.1+f_angle_offset))
            d_x =(3+float(forward_rates[i])/2)*math.cos(a_angle+0.1+f_angle_offset)
            d_y =(3+float(forward_rates[i])/2)*math.sin(a_angle+0.1+f_angle_offset)
            e_x = (c_vec*math.cos(a_angle+0.1+f_angle_offset))
            e_y =(c_vec*math.sin(a_angle+0.1+f_angle_offset))
            tri3 = plt.Polygon(((a_x,a_y),(b_x,b_y),(c_x,c_y)),color='w')
            tri4 = plt.Polygon(((a_x,a_y),(d_x,d_y),(e_x,e_y)),color=col)
            ax.add_patch(tri3)
            ax.add_patch(tri4)

        # input and output arrows below (some scaling and adjustment may be needed)
        # input arrows/swoops
        if is_incoming[i]:
            col = fcolours[i]
            angle = (((90-delta*(i))*(math.pi/180.0))+(90-gap-delta*(i-1))*(math.pi/180.0))/2
            width = transformed_rates_f[i]-3
            style="simple,tail_width=" + str(width)+ ",head_width="+ str(width)+",head_length=0.001"
           # style="wedge,tail_width=" + str(width)+ ",shrink_factor=0.5"
            kw = dict(arrowstyle=style, color=col)

            shift = radial_offsets_f[i]/2
            x1 = (3.0+shift)*math.cos(angle)
            x2 = (4.0+shift)*math.cos(angle + (delta*math.pi/180.0)/4)
            y1 = (3.0+shift)*math.sin(angle)
            y2 = (4.0+shift)*math.sin(angle + (delta*math.pi/180.0)/4)

            arrow = mpatches.FancyArrowPatch((x2,y2),(x1,y1),connectionstyle="arc3,rad=0.3",**kw)
            ax.add_patch(arrow)
        if is_outgoing[i]:
            col = fcolours[i]
            angle = (((90-delta*(i))*(math.pi/180.0))+(90-gap-delta*(i-1))*(math.pi/180.0))/2
            width = transformed_rates_f[i]-3
            style="simple,tail_width=" + str(width)+ ",head_width="+ str(width*2) + ",head_length="+str(width)
           # style="wedge,tail_width=" + str(width)+ ",shrink_factor=0.5"
            kw = dict(arrowstyle=style, color=col)


            edit1 = (delta*math.pi/180.0/3)
            edit2 = (delta*math.pi/180.0/22)
            shift = radial_offsets_f[i]/1.8
            x1 = (3.0+shift)*math.cos(angle + edit1)
            x2 = (4.5+shift)*math.cos(angle + edit2)
            y1 = (3.0+shift)*math.sin(angle + edit1)
            y2 = (4.5+shift)*math.sin(angle + edit2)

            arrow = mpatches.FancyArrowPatch((x1,y1),(x2,y2),connectionstyle="arc3,rad=0.4",**kw)
            ax.add_patch(arrow)
    plt.draw()

    # correct mimetype based on filetype (for displaying in browser)
    if f_format == 'svg':
        mimetype = 'image/svg+xml'
    elif f_format == 'png':
        mimetype = 'image/png'
    else:
        raise ValueError('Image format {} not supported.'.format(format))

    plt.savefig(img, format=f_format)
    plt.close()
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return 'data:{};base64,{}'.format(mimetype, graph_url)




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
