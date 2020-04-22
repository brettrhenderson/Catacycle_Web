from flask import render_template, request, jsonify, make_response, Response, url_for
from werkzeug.utils import secure_filename
from werkzeug.wsgi import FileWrapper
from app.form import RatesForm, DownloadForm
from app.modules.catacycle.oboros import draw, draw_straight
from app.modules.vtna.web_plot import plot_vtna
from app import app
import logging
from app.modules.vtna import vtna_helper as vh

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/cycle', methods=['GET', 'POST'])
def cycle():

    form = RatesForm(request.form)  # initialize the backend of the web form
    data = form.default_data()  # initialize the form with some default data on the front end

    if request.method == 'POST' and form.validate():
        data = form.draw_data()
        log.debug(data)
        return jsonify(data=[draw(data, startrange=0.15, stoprange=0.65,), draw_straight(data, startrange=0.15, stoprange=0.65,)])

    log.debug(data)
    return render_template('cycle.html',
                           graph1=draw(data, startrange=0.15, stoprange=0.65,),
                           graph2=draw_straight(data, startrange=0.15, stoprange=0.65,),
                           rows=data['num_steps'],
                           form=form,
                           form_values=data)

@app.route('/download', methods=['GET', 'POST'])
def download():

    d_form = DownloadForm(request.form)

    if request.method == 'POST' and d_form.validate():
        data = d_form.draw_data()
        log.debug(data)
        if data['image_index'] == 0:
            filename = secure_filename('cycle.{}'.format(data['f_format']))
            img, mimetype = draw(data, startrange=0.15, stoprange=0.65, f_format=data['f_format'], return_image=True)
        else:
            filename = secure_filename('straight.{}'.format(data['f_format']))
            img, mimetype = draw_straight(data, startrange=0.15, stoprange=0.65, f_format=data['f_format'], return_image=True)
        img.seek(0)
        img = FileWrapper(img)
        response = make_response(Response(img, mimetype=mimetype, direct_passthrough=True))
        response.headers.set('Content-Disposition', 'attachment', filename=filename)
        return response
        # return send_file(img, mimetype=mimetype, attachment_filename=filename, as_attachment=True)
    else:
        log.debug("Not sending anything")
        return '', 204

@app.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    return render_template('aboutus.html')

@app.route('/vtna', methods=['GET', 'POST'])
def vtna():
    concs = [1,2]#[0.0510, 0.0578, 0.0688, 0.0750, 0.104, 0.125, 0.127, 0.142]
    rxns = None  # [0, 1]
    species = [1,3] # [0,1]
    trans_zero = [-11.5, -2.1] #[0] * len(concs)  # [-2.5, -12.5]
    win = [25, 5] #[1] * len(concs)
    order = 1
    poison = 0.2
    normalization_method = "TC"

    filename = "app/modules/vtna/sampledata/vtna_multiple.xlsx"
    raw_data, sheet_names = vh.load_raw(filename)
    selected = vh.select_data(raw_data, rxns, species)

    totals = vh.get_sheet_totals(normalization_method, selected)
    norm_data = vh.normalize_columns(selected, totals)

    return render_template('vtna.html',
                           graph1=plot_vtna(norm_data, concs, order=order, poison=poison, trans_zero=trans_zero, windowsize=win,
                                            marker="^", linestyle=':', markersize=5, guide_lines=True))  # colors=None
