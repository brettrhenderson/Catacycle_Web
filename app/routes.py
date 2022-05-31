from flask import render_template, request, jsonify, send_file, redirect, url_for, make_response, Response
from werkzeug.utils import secure_filename
from werkzeug.wsgi import FileWrapper
from werkzeug.datastructures import CombinedMultiDict
from app.catacycle_form import RatesForm, DownloadForm
from app.cake_form import CakeForm, CakeDownloadForm
from app.oboros import draw, draw_straight
import cake as ck
from app import app
import os
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    return render_template('aboutus.html')


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


##########################################
# CAKE
##########################################

@app.route('/cake', methods=['GET', 'POST'])
def cake():
    form = CakeForm()  # initialize the backend of the web form
    log.debug(f'\nFORM VALID? {form.validate()}\n')
    log.debug(f'\nFORM VALIDATION ERRORS: {form.errors.items()}\n')
    log.debug(f'\nFORM DATA {form.data}\n')

    if request.method == 'POST' and form.validate_on_submit():
        log.debug(f"Collected form data from user: {form.data}")

        try:
            cake_data, _ = run_cake_wrapper(form)
        except Exception as e:
            return e.__str__(), 400

        t, r, p, fit, fit_p, fit_r, _, res_val, res_err, ss_res, r_squared, cat_pois, cat_pois_err = cake_data

        html = ck.plot_cake_results(t, r, p, fit, fit_p, fit_r, form.r_col.data, form.p_col.data, f_format='svg',
                                      return_image=False)

        results = ck.pprint_cake(res_val, res_err, ss_res, r_squared, cat_pois, cat_pois_err)

        return jsonify(data=[html, results])

    return render_template('cake.html', form=form)


@app.route('/download-cake-xlsx', methods=['GET', 'POST'])
def download_cake_xlsx():
    log.debug(f"Downloading the Excel data")

    form = CakeForm()

    if request.method == 'POST' and form.validate_on_submit():
        log.debug(f"Collected form data from user: {form.data}")

        try:
            cake_data, df = run_cake_wrapper(form)
        except Exception as e:
            return e.__str__(), 400

        t, r, p, fit, fit_p, fit_r, _, res_val, res_err, ss_res, r_squared, cat_pois, cat_pois_err = cake_data
        t_col, r_col, p_col = get_col_nums(form)
        cat_add_rate = ck.get_cat_add_rate(form.cat_sol_conc.data, form.inject_rate.data, form.react_vol_init.data)
        param_dict = ck.make_param_dict(form.stoich_r.data, form.stoich_p.data, form.r0.data, form.p0.data,
                                          form.p_end.data, cat_add_rate, form.format_k_est(),
                                          form.format_r_ord(), form.format_cat_ord(), form.format_t0_est(), t_col, None,
                                          r_col, p_col, form.max_order.data, form.scale_avg_num.data, form.win.data,
                                          form.inc.data, form.fit_asp.data)

        tmp_file, mimetype = ck.write_fit_data_temp(df, param_dict, t, r, p, fit_p, fit_r, res_val, res_err, ss_res,
                                                      r_squared, cat_pois, cat_pois_err)

        tmp_file.seek(0)
        response = make_response(Response(FileWrapper(tmp_file), mimetype=mimetype, direct_passthrough=True))
        filename = secure_filename('cake_fit.xlsx')
        response.headers.set('Content-Disposition', 'attachment', filename=filename)
        log.debug(response)
        return response
    else:
        log.debug("Not sending anything")
        return '', 204


@app.route('/download-cake', methods=['GET', 'POST'])
def download_cake():

    form = CakeDownloadForm()

    if request.method == 'POST' and form.validate_on_submit():
        log.debug(f"Collected form data from user: {form.data}")

        try:
            cake_data, _ = run_cake_wrapper(form)
        except Exception as e:
            return e.__str__(), 400

        t, r, p, fit, fit_p, fit_r, _, res_val, res_err, ss_res, r_squared, cat_pois, cat_pois_err = cake_data

        img, mimetype = ck.plot_cake_results(t, r, p, fit, fit_p, fit_r, form.r_col.data, form.p_col.data,
                                               f_format=form.f_format.data, return_image=True)
        img.seek(0)
        img = FileWrapper(img)
        response = make_response(Response(img, mimetype=mimetype, direct_passthrough=True))
        filename = secure_filename(f'cake.{form.f_format.data}')
        response.headers.set('Content-Disposition', 'attachment', filename=filename)
        return response
    else:
        log.debug("Not sending anything")
        return '', 204


def get_col_nums(form):
    t_col, r_col, p_col = None, None, None
    if form.t_col.data:
        t_col = form.t_col.data - 1
    if form.r_col.data:
        r_col = form.r_col.data - 1
    if form.p_col.data:
        p_col = form.p_col.data - 1
    return t_col, r_col, p_col


def run_cake_wrapper(form):
    df = ck.read_data(form.xl.data, form.sheet_name.data)
    log.debug(f"Read Data from user-specified Excel sheet:\n {df.head(5)}")

    # reset column indices to 1-indexed
    t_col, r_col, p_col = get_col_nums(form)

    cat_add_rate = ck.get_cat_add_rate(form.cat_sol_conc.data, form.inject_rate.data, form.react_vol_init.data)

    cake_data = ck.fit_cake(df, form.stoich_r.data, form.stoich_p.data, form.r0.data, form.p0.data, form.p_end.data,
                       cat_add_rate, form.format_k_est(), form.format_r_ord(), form.format_cat_ord(),
                       form.format_t0_est(), t_col, None, r_col, p_col, form.max_order.data,
                       form.scale_avg_num.data, form.win.data, form.inc.data, form.fit_asp.data)

    return cake_data, df
