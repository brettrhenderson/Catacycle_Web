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

fcolours = "#4286f4 #e2893b #de5eed #dd547d #4ee5ce #4286f4 #dd547d #4ee5ce #4286f4 #dd547d #4ee5ce".split()
rcolours = "#82abed #efb683 #edb2f4 #ef92ae #91f2e3 #82abed #ef92ae #91f2e3 #82abed #ef92ae #91f2e3".split()


def draw(data=None):
    img = io.BytesIO()

    forward_rates = []
    rev_rates = []

    gap = 5  # default gap without settings
    scale = 23.9   # will scale pending on image size -- connects graph space to figure space

    # Different image size scale will need to be coded in using "transformed_point = ax.transData.transform((x,y))"
    if data is None:
        data = open("data.dat", 'r')
        for line in data:
            if "f_rate" in line:
                forward_rates.append(line.split()[2])
            if "r_rate" in line:
                rev_rates.append(line.split()[2])
            if "gap" in line:
                gap = float(line.split()[2])

    else:
        for i in range(1,11):
            f_rate = data['f_rate{}'.format(i)]
            if f_rate > 0.0:
                forward_rates.append(f_rate)
                rev_rates.append(data['r_rate{}'.format(i)])

    # call Sofia's Scaler function, convert rates to arrow size
    forward_rates, rev_rates = scaler(forward_rates, rev_rates, small_arrow=0.1, big_arrow=0.8, logarythmic=False)

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
    for i in range(0,num_segments):
        radial_offsets_f.append(float(forward_rates[i])/2)
        radial_offsets_r.append(float(rev_rates[i])/2)
        transformed_rates_f.append(float(forward_rates[i])*scale)
        transformed_rates_r.append(float(rev_rates[i])*scale)


    # Drawing outside and inside curves
    for i in range(0,num_segments):
        if fcolours[i] == "blank":
            r = lambda: random.randint(0,255)
            col = ('#%02X%02X%02X' % (r(),r(),r()))
        else:
            col = fcolours[i]
        Curve = mpatches.Arc((0,0),height=6+radial_offsets_f[i],width=6+radial_offsets_f[i],angle=1,
                             theta1=90-delta*i,theta2=90-gap-delta*(i-1),linewidth=transformed_rates_f[i],color=col)
        ax.add_patch(Curve)
        col = rcolours[i]
        Curve = mpatches.Arc((0,0),height=6-radial_offsets_r[i],width=6-radial_offsets_r[i],angle=1,theta1=90-delta*i,
                             theta2=90-gap-delta*(i-1),linewidth=transformed_rates_r[i],color=col)
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
        c_vec = (3+(float(forward_rates[i])+(float(forward_rates[i])/4)))
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

    # Inside Arrows
        if rev_rates[i] != 0:
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
                                 theta1=90-delta*i,theta2=90-gap-delta*(i-1),linewidth=transformed_rates_f[i],color=col)
            ax.add_patch(Curve)
            a_x = 3*math.cos(a_angle)
            a_y = 3*math.sin(a_angle)
            b_vec = (3-(float(forward_rates[i])))
            c_vec = (3+(float(forward_rates[i])+(float(forward_rates[i])/4)))
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

        # plt.text(4*math.cos(b_angle-0.1-r_angle_offset),4*math.sin(b_angle-0.1-r_angle_offset),"test")

    plt.draw()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)


print("running")

# transforming rates to line widths:
# range = [0.1, 0.8], size = 0.7
# find max and min of f_rate and r_rate
# subtract smallest rate, multiply by 0.8/(max-min), add 0.1
def scaler(forward_rates, rev_rates, small_arrow=0.1, big_arrow=0.8, logarythmi
    forward_rates = np.array(forward_rates).astype(np.float)
    rev_rates = np.array(rev_rates).astype(np.float)

    if logarythmic:
        forward_rates[np.nonzero(forward_rates)] = np.log10(forward_rates[np.nonzero(forward_rates)])
        rev_rates[np.nonzero(rev_rates)] = np.log10(rev_rates[np.nonzero(rev_rates)])

    f_min = np.min(forward_rates[np.nonzero(forward_rates)])
    f_max = forward_rates.max()
    r_max = rev_rates.max()
    if r_max == 0:
        r_min = f_min
    else:
        r_min = np.min(rev_rates[np.nonzero(rev_rates)])

    maxima = max(f_max, r_max)
    minima = min(f_min, r_min)

    ranger = big_arrow - small_arrow

    # incase k range = 0
    if minima == maxima:
        forward_rates = (forward_rates * 0.0  np.mean([big_arrow, small_arrow]
    else:
        forward_rates = ((forward_rates - minima) / (maxima - minima) * ranger

    # incase reverse is empty
    if r_max == 0:
        print('all 0 oo')
        rev_rates = (rev_rates).tolist()
    else:
    minima = min(f_min, r_min)

    ranger = big_arrow - small_arrow

    # incase k range = 0
    if minima == maxima:
        forward_rates = (forward_rates * 0.0 + np.mean([big_arrow, small_arrow])).tolist()
    else:
        forward_rates = ((forward_rates - minima) / (maxima - minima) * ranger + small_arrow).tolist()

    # incase reverse is empty
    if r_max == 0:
        print('all 0 oo')
        rev_rates = (rev_rates).tolist()
    else:
        rev_rates[np.nonzero(rev_rates)] = (
                    (rev_rates[np.nonzero(rev_rates)] - minima) / (maxima - minima) * ranger + small_arrow)
        rev_rates = rev_rates.tolist()
    print(rev_rates)
    print(forward_rates)
    return forward_rates, rev_rates
