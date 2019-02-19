from flask import render_template, request, jsonify
from app.form import RatesForm
from app.oboros import draw
from app import app
import logging

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    form = RatesForm(request.form)  # initialize the backend of the web form
    data = form.default_data()  # initialize the form with some default data on the front end

    if request.method == 'POST' and form.validate():
        data = form.draw_data()
        log.debug('gap: {}'.format(data['gap']))
        log.debug('scale type: {}'.format(data['scale_type']))
        log.debug('thickness: {}'.format(data['thickness']))
        return jsonify(data=draw(data))

    # log.debug('gap: {}'.format(data['gap']))
    # log.debug('scale type: {}'.format(data['scale_type']))
    # log.debug('thickness: {}'.format(data['thickness']))

    return render_template('graphs.html',
                           graph1=draw(data),
                           rows=data['num_steps'],
                           form=form,
                           form_values=data)
