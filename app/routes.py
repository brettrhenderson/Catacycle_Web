from flask import render_template, request
from app.form import RatesForm
from app.oboros import draw
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    rows = 4  # default give table 4 rows
    form = RatesForm(request.form)  # initialize the backend of the web form
    data = form.default_data()  # initialize the form with some default data on the front end
    if request.method == 'POST' and form.validate():
        # print(form.validate())
        # print(form.errors)
        rows = form.num_rows()
        data = form.rates()
    graph1_url = draw(data)
    return render_template('graphs.html',
                           graph1=graph1_url,
                           form=form,
                           rows=rows,
                           form_values=data)
