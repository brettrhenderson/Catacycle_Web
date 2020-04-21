import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
from flask import url_for
from app.modules.vtna import vtna_helper as vh


def plot_vtna(data,  concs, order=1, trans_zero=None,  windowsize=None, colors=None, marker_shape="o", markersize=15,
              linestyle=':', guide_lines=True, f_format='png', return_image=False):
    """Plot the Aligned Reaction Traces"""
    if data is None:
        return url_for('.static', filename='images/1orderrxn2.png')
    if trans_zero is None:
        trans_zero = [0]*len(data)
    if windowsize is None:
        windowsize = [1]*len(data)
    # set defaults and declare variables
    img = io.BytesIO()  # file-like object to hold image

    #put ipynb fn here to plot fitted graph once order etc. is known
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, autoscale_on=True) #, xlim=(0, 20), ylim=(-0.1, 1.1))
    maxtime = max(vh.get_max_times(data))
    for i, rxn in enumerate(data):
        for j, col in enumerate(rxn.columns):
            if j > 0:
                t_vtna = (rxn.iloc[:, 0] + trans_zero[i]) * float(concs[i]) ** order
                smoothed = rxn.loc[:, col].rolling(windowsize[i], center=True).mean()
                ax.plot(t_vtna, smoothed, marker=marker_shape, linestyle=linestyle, markersize=markersize)

    if guide_lines:
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        ax.vlines(0, 0, 1, linestyle=':', linewidth=1, color='k')
        ax.hlines(0, xmin, xmax, linestyle=':', linewidth=1, color='k')
        ax.hlines(1, xmin, xmax, linestyle=':', linewidth=1, color='k')
    ax.set_xlabel('time', fontsize=16)
    ax.set_ylabel('Relative Abundance', fontsize=16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    #plt.tight_layout()

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

    plt.draw()
    plt.savefig(img, format=f_format, transparent=True)
    plt.close()
    img.seek(0)

    if not return_image:
        graph_url = base64.b64encode(img.getvalue()).decode()
        return 'data:{};base64,{}'.format(mimetype, graph_url)
    else:
        return img, mimetype
