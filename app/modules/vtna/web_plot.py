import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
from flask import url_for
from app.modules.vtna import vtna_helper as vh
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def plot_vtna(data, concs=None, norm_time=False, orders=None, trans_zero=None,  windowsize=None, colors=None, legend=True,
              guide_lines=True, f_format='svg', **kwargs):
    """Plot the Aligned Reaction Traces"""
    log.debug("Closed all figures!")
    if trans_zero is None:
        trans_zero = [0]*len(data)
    if windowsize is None:
        windowsize = [1]*len(data)
    # set defaults and declare variables
    img = io.BytesIO()  # file-like object to hold image

    #put ipynb fn here to plot fitted graph once order etc. is known
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, autoscale_on=True) #, xlim=(0, 20), ylim=(-0.1, 1.1))
    maxtime = max(vh.get_max_times(data))
    for i, rxn in enumerate(data):
        if norm_time:
            # t_vtna = (rxn.iloc[:, 0] + trans_zero[i]) * float(concs[i]) ** orders
            log.debug(f"concs: {concs[i]}")
            log.debug(f"orders: {orders}")
            log.debug(f"Original Time: {rxn.iloc[:, 0].values + trans_zero[i]}")
            t_vtna = vh.time_norm(rxn.iloc[:, 0].values + trans_zero[i], concs[i], orders)
            log.debug(f"Normalized Time: {t_vtna}")
        else:
            t_vtna = rxn.iloc[:, 0] + trans_zero[i]
        for j, col in enumerate(rxn.columns):
            if j > 0:
                smoothed = rxn.loc[:, col].rolling(windowsize[i], center=True).mean()
                ax.plot(t_vtna, smoothed, label=f"rxn{i+1}, spec{j}", **kwargs)

    if guide_lines:
        add_guidelines(ax)

    if legend:
        ax.legend()

    format_ax(ax)
    plt.tight_layout()

    # save to bytes-like object
    plt.savefig(img, format=f_format, transparent=True)
    img.seek(0)

    # correct mimetype based on filetype (for displaying in browser)
    mimetype = get_mime(f_format)

    # if downloading image, return the bytes directly
    graph_url = base64.b64encode(img.getvalue()).decode()
    #return 'data:{};base64,{}'.format(mimetype, graph_url), fig
    return 'data:{};base64,{}'.format(mimetype, graph_url), fig


def format_ax(ax):
    ax.set_xlabel('time', fontsize=16)
    ax.set_ylabel('Relative Abundance', fontsize=16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

def get_mime(f_format):
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
    return mimetype


def add_guidelines(ax):
    xmin, xmax = ax.get_xlim()
    ax.vlines(0, 0, 1, linestyle=':', linewidth=1, color='k')
    ax.hlines(0, xmin, xmax, linestyle=':', linewidth=1, color='k')
    ax.hlines(1, xmin, xmax, linestyle=':', linewidth=1, color='k')


def save_dfig(fig, f_format):
    img = io.BytesIO()  # file-like object to hold image
    # save to bytes-like object
    fig.savefig(img, format=f_format, transparent=True)
    # correct mimetype based on filetype (for displaying in browser)
    mimetype = get_mime(f_format)
    return img, mimetype
