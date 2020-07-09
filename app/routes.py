from flask import render_template, request, jsonify, send_file, redirect, url_for, make_response, Response
from werkzeug.utils import secure_filename
from werkzeug.wsgi import FileWrapper
from app.form import RatesForm, DownloadForm
from app.oboros import draw, draw_straight
from app import app
import os
import logging

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    form = RatesForm(request.form)  # initialize the backend of the web form
    data = form.default_data()  # initialize the form with some default data on the front end

    log.debug(f'\nFORM VALID? {form.validate()}\n')
    log.debug(f'\nFORM VALIDATION ERRORS: {form.errors.items()}\n')

    if request.method == 'POST' and form.validate():
        data = form.draw_data()
        log.debug(f"\nNEW DATA: {data}\n")
        log.debug(f'relative: {form.head_len_relative.data}')
        return jsonify(data=[draw(data, startrange=0.15, stoprange=0.8,), draw_straight(data, startrange=0.15, stoprange=0.8,)])

    log.debug(f"\nDEFAULT DATA: {data}\n")
    return render_template('graphs.html',
                           graph1=draw(data, startrange=0.15, stoprange=0.8,),
                           graph2=draw_straight(data, startrange=0.15, stoprange=0.8,),
                           rows=data['data1']['num_steps'],
                           form=form,
                           form_values=data['data1'])


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
        log.debug(response)
        return response
        # return send_file(img, mimetype=mimetype, attachment_filename=filename, as_attachment=True)
    else:
        log.debug("Not sending anything")
        return '', 204
