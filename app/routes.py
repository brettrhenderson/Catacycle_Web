from flask import render_template, request
from app.form import RatesForm
from app.oboros import draw
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    form = RatesForm(request.form)  # initialize the backend of the web form
    data = form.default_data()  # initialize the form with some default data on the front end
    if request.method == 'POST' and form.validate():
        pass
        # print(form.validate())
        # print(form.errors)
        data = form.draw_data()

    graph1_url = draw(data)
    return render_template('graphs.html',
                           graph1=graph1_url,
                           rows=form.num_steps.data,
                           form=form,
                           form_values=data)
