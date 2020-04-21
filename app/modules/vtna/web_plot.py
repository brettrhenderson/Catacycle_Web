import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
from flask import url_for



def plot_vtna(data=None, order=1, f_format='svg', return_image=False):
    """Plot the Aligned Reaction Traces"""
    if data is None:
        return url_for('.static', filename='images/1orderrxn2.svg')

    # set defaults and declare variables
    img = io.BytesIO()  # file-like object to hold image


    #put ipynb fn here to plot fitted graph once order etc. is known



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
