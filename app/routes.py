from flask import render_template, request
from app.form import RatesForm
from app.oboros import draw
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    has_data = False
    rows = 4  # default give table 4 rows
    form = RatesForm(request.form)  # initialize the backend of the web form
    data = form.no_data()  # initialize the form with no data on the front end
    if request.method == 'POST' and form.validate():
        # print(form.validate())
        # print(form.errors)
        rows = form.num_rows()
        data = form.values()
        has_data = True
    if has_data:
        graph1_url = draw(data)
    else:
        graph1_url = draw()  # draw with the default data.dat file if there is no user input
    return render_template('graphs.html',
                           graph1=graph1_url,
                           form=form,
                           rows=rows,
                           form_values=data)
