from flask import render_template, request, jsonify, make_response, Response, session
from app import app
from werkzeug.utils import secure_filename
from werkzeug.wsgi import FileWrapper
from app.cycleform import RatesForm, DownloadForm
from app.vtnaform import VTNAForm, DataForm
from app.modules.catacycle.oboros import draw, draw_straight
from app.modules.vtna.web_plot import plot_vtna
import logging
from app.modules.vtna import vtna_helper as vh
import os

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

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
    concs = [0.0510,0.0578,0.0688,0.0750,0.104,0.125,0.127,0.142]
    rxns = None  # [0, 1]
    species = None  # [0,1]
    trans_zero = [0]*len(concs)  # [-2.5, -12.5]
    win = [1] * len(concs)
    order = 0
    filename = "app/static/sampledata/Hydroamination-Kinetics-Catalyst-Order.xlsx"
    raw_data, sheet_names = vh.load_raw(filename)
    totals = vh.get_sheet_totals(None, raw_data)
    norm_data = vh.normalize_columns(raw_data, totals)
    gimme = vh.select_data(norm_data, rxns, species)

    file_form = DataForm()
    format_form = VTNAForm()

    return render_template('vtna.html',
                           form=format_form,
                           fileform=file_form,
                           graph1=plot_vtna(gimme, concs, order=order, trans_zero=trans_zero, windowsize=win,
                                            marker_shape="^", linestyle=':', markersize=5, guide_lines=True))

@app.route('/upload', methods=['POST'])
def upload_data():
    xlform = DataForm()
    log.debug(f"Sent to the right endpoint! \n file_form: {xlform.xl.data.filename}\n")
    if request.method == 'POST':
        if xlform.validate():
            f = xlform.xl.data
            raw_data, sheet_names = vh.load_raw(f)
            session['raw_data'] = raw_data
            session['sheet_names'] = sheet_names
            fb = f"Successfully uploaded {f.filename}"
            result = f"This file contains {len(raw_data)} reactions " \
                    f"and {raw_data[0].shape[1]-1} monitored species."
            category = "success"
        else:
            fb = f"Upload failed: {xlform.xl.errors}"
            result = ""
            category = "danger"
        return make_response(jsonify(feedback=fb, category=category, result=result), 200)

@app.route('/format', methods=['POST'])
def format_plot():
    format_form = VTNAForm()
    if request.method == 'POST' and format_form.validate():
        log.debug("Submitted formatting form")