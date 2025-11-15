from flask import render_template, request, jsonify, send_file, redirect, url_for, make_response, Response
from werkzeug.utils import secure_filename
from werkzeug.wsgi import FileWrapper
from app.catacycle_form import RatesForm, DownloadForm
from app.cake_form import CakeForm, CakeDownloadForm
from app.cc_form import CCForm, CCDownloadForm
from app.oboros import draw, draw_straight
import app.outputs as outputs
import cake as ck
import continuous_calibration

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


@app.route('/user-guide', methods=['GET', 'POST'])
def guide():
    return render_template('guide.html')


##############################################
# CATACYCLE
##############################################

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


##############################################
# CAKE
##############################################

@app.route('/cake', methods=['GET', 'POST'])
def cake():
    form = CakeForm()  # initialize the backend of the web form
    data = form.data
    log.debug(f'\nFORM VALID? {form.validate()}\n')
    log.debug(f'\nFORM VALIDATION ERRORS: {form.errors.items()}\n')
    log.debug(f'\nFORM DATA {data}\n')

    if request.method == 'POST' and form.validate_on_submit():
        try:
            sim = data['upload']['sim']
            if sim:
                dict, sim_data = run_cake_sim_wrapper(form)
                html, _ = sim_data.plot_conc_vs_time(f_format='svg', return_img=False)
                results = f"""Simulation completed
                
Download file to see full results"""
            else:
                dict, df, fit_data = run_cake_fit_wrapper(form)
                html, _ = fit_data.plot_conc_vs_time(f_format='svg', return_img=False)
                results = outputs.pprint_cake(fit_data)
        except Exception as e:
            raise e

        return jsonify(data=[html, results])

    return render_template('cake.html', form=form)


@app.route('/download-cake-xlsx', methods=['GET', 'POST'])
def download_cake_xlsx():
    log.debug(f"Downloading the Excel data")
    form = CakeForm()
    data = form.data
    log.debug(f'\nFORM VALID? {form.validate()}\n')
    log.debug(f'\nFORM VALIDATION ERRORS: {form.errors.items()}\n')
    log.debug(f'\nFORM DATA {data}\n')

    if request.method == 'POST' and form.validate_on_submit():
        try:
            sim = data['upload']['sim']
            if sim:
                dict, sim_data = run_cake_sim_wrapper(form)
                tmp_file, mimetype = outputs.write_cake_sim_data_temp(dict, sim_data)
                filename = secure_filename('cake_sim.xlsx')
            else:
                dict, df, fit_data = run_cake_fit_wrapper(form)
                tmp_file, mimetype = outputs.write_cake_fit_data_temp(dict, fit_data)
                filename = secure_filename('cake_fit.xlsx')
        except Exception as e:
            raise e

        tmp_file.seek(0)
        response = make_response(Response(FileWrapper(tmp_file), mimetype=mimetype, direct_passthrough=True))
        response.headers.set('Content-Disposition', 'attachment', filename=filename)
        log.debug(response)
        return response
    else:
        log.debug("Not sending anything")
        return '', 204


@app.route('/download-cake', methods=['GET', 'POST'])
def download_cake():
    form = CakeDownloadForm()
    data = form.data
    img_format = data['f_format']

    if request.method == 'POST' and form.validate_on_submit():
        try:
            sim = data['upload']['sim']
            if sim:
                dict, sim_data = run_cake_sim_wrapper(form)
                img, mimetype = sim_data.plot_fit_results(f_format=img_format, retun_img=True)
            else:
                dict, df, fit_data = run_cake_fit_wrapper(form)
                img, mimetype = fit_data.plot_fit_results(f_format=img_format, retun_img=True)
        except Exception as e:
            raise e

        img.seek(0)
        img = FileWrapper(img)
        response = make_response(Response(img, mimetype=mimetype, direct_passthrough=True))
        filename = secure_filename(f'cake.{img_format}')
        response.headers.set('Content-Disposition', 'attachment', filename=filename)
        return response
    else:
        log.debug("Not sending anything")
        return '', 204


def run_cake_fit_wrapper(form):
    dict = form.prepare_data()

    log.debug(f"FORMATTED DATA: {dict}")

    df = ck.import_data(dict['xl'], dict['sheet_name'], dict['t_col'], dict['col'], dict['temp_col'])
    blank_dict = {'rxns': None, 'tic_col': None, 'time_unit':'time_unit',
                  'conc_unit':'moles_unit volume_unit$^{-1}$'}
    fit_output = ck.fit(df, *[{**dict, **blank_dict}[key] for key in ['spec_name', 'spec_type', 'stoich', 'rxns',
        't_col', 'col', 'fit_asp', 'mol0', 'mol_end', 'vol0', 'add_sol_conc', 'add_cont_rate', 't_cont', 'add_one_shot',
        't_one_shot', 'sub_cont_rate', 'sub_aliq', 't_aliq', 'temp0', 'temp_cont', 't_temp', 'temp_col', 'rate_eq_type',
        'rate_method', 'rtol', 'atol', 'k_lim', 'ord_lim', 'pois_lim', 'scale_avg_num', 'win', 'inc', 'tic_col',
        'time_unit', 'conc_unit']])

    return dict, df, fit_output


def run_cake_sim_wrapper(form):
    dict = form.prepare_data(sim=True)

    log.debug(f"FORMATTED DATA: {dict}")

    blank_dict = {'rxns': None, 'rand_fac': None, 'scale': 1, 'time_unit':'time_unit',
                  'conc_unit':'moles_unit volume_unit$^{-1}$'}
    sim_output = ck.sim(*[{**dict, **blank_dict}[key] for key in ['t', 'spec_name', 'spec_type', 'stoich', 'rxns',
        'mol0', 'vol0', 'add_sol_conc', 'add_cont_rate', 't_cont', 'add_one_shot', 't_one_shot', 'sub_cont_rate',
        'sub_aliq', 't_aliq', 'temp0', 'temp_cont', 't_temp', 'rate_eq_type', 'rate_method', 'rtol', 'atol', 'k_lim',
        'ord_lim', 'pois_lim', 'inc', 'rand_fac', 'scale', 'time_unit', 'conc_unit']])

    return dict, sim_output


##############################################
# Continuous Calibration
##############################################

@app.route('/cc', methods=['GET', 'POST'])
def cc():
    form = CCForm()  # initialize the backend of the web form
    data = form.data
    log.debug(f'\nFORM VALID? {form.validate()}\n')
    log.debug(f'\nFORM VALIDATION ERRORS: {form.errors.items()}\n')
    log.debug(f'\nFORM DATA {data}\n')

    if request.method == 'POST' and form.validate_on_submit():
        try:
            dict, gen_df, gen_output, apply_df, apply_output = run_cc_wrapper(form)
        except Exception as e:
            raise e
            # return e.__str__(), 400

        if apply_output is not None:
            html, _ = apply_output.plot_conc_vs_time(f_format='svg', return_img=False)
        else:
            html, _ = gen_output.plot_intensity_vs_conc(f_format='svg', return_img=False)

        results = outputs.pprint_cc(gen_output)

        return jsonify(data=[html, results])

    return render_template('cc.html', form=form)


@app.route('/download-cc-xlsx', methods=['GET', 'POST'])
def download_cc_xlsx():
    log.debug(f"Downloading the Excel data")
    form = CCForm()
    data = form.data
    log.debug(f'\nFORM VALID? {form.validate()}\n')
    log.debug(f'\nFORM VALIDATION ERRORS: {form.errors.items()}\n')
    log.debug(f'\nFORM DATA {data}\n')
    if request.method == 'POST' and form.validate_on_submit():
        try:
            dict, gen_df, gen_output, apply_df, apply_output = run_cc_wrapper(form)
        except Exception as e:
            raise e
        log.debug(dict)
        tmp_file, mimetype = outputs.write_cc_fit_data_temp(dict, gen_output, apply_output)
        filename = secure_filename('cc.xlsx')

        tmp_file.seek(0)
        response = make_response(Response(FileWrapper(tmp_file), mimetype=mimetype, direct_passthrough=True))
        response.headers.set('Content-Disposition', 'attachment', filename=filename)
        log.debug(response)
        return response
    else:
        log.debug("Not sending anything")
        return '', 204


@app.route('/download-cc', methods=['GET', 'POST'])
def download_cc():
    form = CCDownloadForm()
    data = form.data
    img_format = data['f_format']

    if request.method == 'POST' and form.validate_on_submit():
        try:
            dict, gen_df, gen_output, apply_df, apply_output = run_cc_wrapper(form)
        except Exception as e:
            raise e

        if apply_output is not None:
            img, mimetype = apply_output.plot_conc_vs_time(f_format=img_format, return_img=True)
        else:
            img, mimetype = gen_output.plot_intensity_vs_conc(f_format=img_format, return_img=True)

        img.seek(0)
        img = FileWrapper(img)
        response = make_response(Response(img, mimetype=mimetype, direct_passthrough=True))
        filename = secure_filename(f'cc.{img_format}')
        response.headers.set('Content-Disposition', 'attachment', filename=filename)
        return response
    else:
        log.debug("Not sending anything")
        return '', 204


def run_cc_wrapper(form):
    dict = form.prepare_data()

    log.debug(f"FORMATTED DATA: {dict}")

    gen_df = continuous_calibration.raw_import(dict['gen_xl'], dict['gen_sheet_name'], dict['gen_t_col'],
                                               dict['gen_col'])
    gen_output = continuous_calibration.gen(gen_df, *[{**dict, 'fit_lim': None}[key] for key in ['spec_name',
        'gen_t_col', 'gen_col', 'mol0', 'vol0', 'add_sol_conc', 'add_cont_rate', 't_cont', 'add_one_shot', 't_one_shot',
        'sub_cont_rate', 'path_length', 'fit_eq', 'intercept', 'fit_lim', 'lof_test', 'lof_method', 'p_thresh',
        'lod_stds', 'smooth_eq', 'sg_win', 'breakpoint_lim', 'diffusion_delay', 'zero', 'win', 'inc']])

    if dict['apply_xl'] is not None:
        apply_df = continuous_calibration.raw_import(dict['apply_xl'], dict['apply_sheet_name'], dict['apply_t_col'],
                                                     dict['apply_col'])
        apply_output = gen_output.apply(apply_df, dict['apply_col'], dict['apply_t_col'])
    else:
        apply_df, apply_output = None, None

    return dict, gen_df, gen_output, apply_df, apply_output
