from flask import render_template, request, jsonify, make_response, Response, session
from app import app
from werkzeug.utils import secure_filename
from werkzeug.wsgi import FileWrapper
from app.cycleform import RatesForm, DownloadForm
from app.vtnaform import DataForm, SelectDataForm, DVTNAForm, ManualFitForm, AutoFitForm, FitParamFormTemplate, FitParamForm, StyleForm
from app.modules.catacycle.oboros import draw, draw_straight
from app.modules.vtna.web_plot import plot_vtna, save_dfig
import logging
from app.modules.vtna import vtna_helper as vh
import os, uuid, matplotlib, pickle
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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
        return jsonify(data=[draw(data, startrange=0.15, stoprange=0.65,), draw_straight(data, startrange=0.15,
                                                                                         stoprange=0.65,)])

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

    filename = "app/static/sampledata/Hydroamination-Kinetics-Catalyst-Order.xlsx"
    raw_data, sheet_names, specs = vh.load_raw(filename)
    totals = vh.get_sheet_totals(None, raw_data)
    norm_data = vh.normalize_columns(raw_data, totals)

    upload_form, dform, sform, mform, aform, pformt, pform, stform = (DataForm(), DVTNAForm(), SelectDataForm(), ManualFitForm(),
                                                              AutoFitForm(), FitParamFormTemplate(), FitParamForm(), StyleForm())

    new_plot, fig = plot_vtna(norm_data, marker="^", linestyle=':', markersize=5, guide_lines=False,
                              legend=True)
    path = os.path.join(app.config['DOWNLOADS'], str(uuid.uuid4()))
    # save the filename and pickle the figure
    pickle.dump(fig, open(path, 'wb'))
    plt.close(fig)
    session['fig'] = path
    log.debug(f'Current Figures: {plt.get_fignums()}')

    return render_template('vtna.html', upform=upload_form, dform=dform, sform=sform, aform=aform, mform=mform,
                           pformt=pformt, pform=pform, stform=stform, graph1=new_plot)


@app.route('/upload', methods=['POST'])
def upload_data():
    xlform = DataForm()
    log.debug(f"Sent to the right endpoint! \n file_form: {xlform.xl.data.filename}\n")
    if request.method == 'POST':
        result = ""
        category = "danger"
        new_plot = "none"
        rxns = "none"
        specs = "none"
        if xlform.validate():
            f = xlform.xl.data
            try:
                raw_data, rxns, specs = vh.load_raw(f)
                session['raw_data'] = raw_data
                session['rxns'] = rxns
                session['reactants'] = specs
                session['normtype'] = xlform.normtype.data
                session['starts'] = [0 for rxn in rxns]
                session['poisons'] = None
                session['orders'] = None
                session['excess'] = [False for spec in specs]
                session['concs'] = None
                session['rxns_sel'] = [i for i, _ in enumerate(rxns)]
                session['specs_sel'] = [i for i, _ in enumerate(specs)]
                session['legend'] = True
                session['guidelines'] = False
                session['linewidth'] = 2
                session['linestyle'] = ':'
                session['marker'] = '^'
                session['markersize'] = 5
                session['conc_multipliers'] = None

                fb = f"Successfully uploaded {f.filename}<br>Found {len(raw_data)} reactions and " \
                         f"{raw_data[0].shape[1] - 1} monitored species in this file."
                category = "success"
                log.debug(f"Rxns: {rxns},  Species: {specs}")
                totals = vh.get_sheet_totals(session['normtype'], raw_data)
                norm_data = vh.normalize_columns(raw_data, totals)
                new_plot, fig = plot_vtna(norm_data, norm_time=False, marker="^", linestyle=':', markersize=5,
                                          linewidth=2, guide_lines=False, legend=True)
                # save the filename and pickle the figure
                pickle.dump(fig, open(session['fig'], 'wb'))
                plt.close(fig)
                log.debug(f'Current Figures: {plt.get_fignums()}')
            except ValueError as e:
                fb = f"Upload failed: {e}"
        else:
            fb = f"Upload failed: {xlform.xl.errors}"
        return make_response(jsonify(feedback=fb, rxns=rxns, specs=specs, category=category, new_plot=new_plot,
                                     rxns_sel=session['rxns_sel'], specs_sel=session['specs_sel']), 200)

@app.route('/select', methods=['POST'])
def select_data():
    selectform = SelectDataForm()
    rxns = session['rxns']
    specs = session['reactants']

    selectform.rxn.choices = [(str(i), str(i)) for i, _ in enumerate(rxns)]
    selectform.species.choices = [(str(i), str(i)) for i, _ in enumerate(specs)]

    if request.method == 'POST':
        category = "danger"
        new_plot = "none"
        starts = session['starts']
        raw_data = session['raw_data']
        normtype = session['normtype']
        orders = session['orders']
        concs = session['concs']
        normtime = True if concs is not None else False
        legend = session['legend']
        guidelines = session['guidelines']
        lw = session['linewidth']
        ls = session['linestyle']
        m = session['marker']
        ms = session['markersize']

        if selectform.validate():
            log.debug(f"Selected >> Rxns: {selectform.rxn.data},  Species: {selectform.species.data}")
            rxns_sel = [int(rxn) for rxn in selectform.rxn.data]
            specs_sel = [int(spec) for spec in selectform.species.data]
            if not len(rxns_sel):
                rxns_sel = [i for i, _ in enumerate(rxns)]
            if not len(specs_sel):
                specs_sel = [i for i, _ in enumerate(specs)]
            session['rxns_sel'] = rxns_sel
            session['specs_sel'] = specs_sel

            category = "success"
            log.debug(f"Selected >> Rxns: {session['rxns_sel']},  Species: {specs_sel}")
            totals = vh.get_sheet_totals(normtype, raw_data)
            norm_data = vh.shift_times(vh.normalize_columns(raw_data, totals), starts)
            select_data = vh.select_data(norm_data, reactions=rxns_sel, species=specs_sel)

            log.debug(f'rxns: {rxns_sel}, specs: {specs_sel}, concs shape: {concs}, orders shape: {orders}')
            if concs is not None and rxns_sel[-1] >= len(concs):
                conc_multipliers = session['conc_multipliers']
                poisons = session['poisons']
                param_specs = session['param_specs']
                # re-create the concs data from the save raw data
                # Get the concentrations to normalize by
                concs = [[] for _ in select_data]

                for i, rxn in enumerate(select_data):
                    for j, spec in enumerate(param_specs):
                        if spec == "None":  # This means it is an excess reagent / catalyst
                            concs[i].append([conc_multipliers[j][i] - poisons[j] for _ in range(rxn.values.shape[0])])
                        else:
                            concs[i].append(list(rxn.iloc[:, j + 1].values - poisons[j]))
                log.debug(concs)
                for i, rxn_concs in enumerate(concs):
                    concs[i] = np.array(rxn_concs).T
            else:
                concs_new = []
                if concs is not None:
                    for rx in rxns_sel:
                        try:
                            concs_new.append(concs[rx])
                        except IndexError as e:
                            pass
                concs = concs_new

            new_plot, fig = plot_vtna(select_data, norm_time=normtime, concs=concs, orders=orders, marker=m,
                                      linestyle=ls, markersize=ms, linewidth=lw, guide_lines=False, legend=True)

            # save the filename and pickle the figure
            pickle.dump(fig, open(session['fig'], 'wb'))
            plt.close(fig)
            log.debug(f'Current Figures: {plt.get_fignums()}')
            fb = "Selected data plotted!"
        else:
            fb = f"Data selection failed: {selectform.errors}"
        return make_response(jsonify(feedback=fb, rxns=rxns, specs=specs, category=category, new_plot=new_plot,
                                     rxns_sel=rxns_sel, specs_sel=specs_sel), 200)

@app.route('/set_start', methods=['POST'])
def set_start():
    fitform = ManualFitForm()
    if request.method == 'POST':
        result = ""
        category = "danger"
        new_plot = "none"
        rxns = "none"
        specs = "none"
        if fitform.validate():
            start = fitform.start.data
            session['start'] = start
            order = fitform.order.data
            poison = fitform.poison.data
            raw_data = session['raw_data']
            rxns = session['rxns']
            specs = session['reactants']
            normtype = session['normtype']
            rxns_sel = session['rxns_sel']
            specs_sel = session['specs_sel']
            legend = session['legend']
            guidelines = session['guidelines']
            lw = session['linewidth']
            ls = session['linestyle']
            m = session['marker']
            ms = session['markersize']
            category = "success"
            log.debug(f"Rxns: {rxns},  Species: {specs}")
            totals = vh.get_sheet_totals(normtype, raw_data)
            norm_data = vh.shift_times(vh.normalize_columns(raw_data, totals), start)
            select_data = vh.select_data(norm_data, reactions=rxns_sel, species=specs_sel)
            new_plot, fig = plot_vtna(select_data, norm_time=False, marker=m, linestyle=ls, markersize=ms,
                                      linewidth=lw, guide_lines=guidelines, legend=legend)
            # save the filename and pickle the figure
            pickle.dump(fig, open(session['fig'], 'wb'))
            plt.close(fig)
            log.debug(f'Current Figures: {plt.get_fignums()}')
            fb = "Updated Manual VTNA Fit"
        else:
            fb = f"Update failed: {fitform.errors}"
        return make_response(jsonify(feedback=fb, rxns=rxns, specs=specs, category=category, new_plot=new_plot,
                             rxns_sel=rxns_sel, specs_sel=specs_sel), 200)




@app.route('/fit', methods=['POST'])
def fit_data():
    fitform = FitParamForm()

    if request.method == 'POST':
        result = ""
        category = "danger"
        starts = session['starts']
        raw_data = session['raw_data']
        rxns = session['rxns']
        normtype = session['normtype']
        rxns_sel = session['rxns_sel']
        specs_sel = session['specs_sel']
        specs = session['reactants']
        legend = session['legend']
        guidelines = session['guidelines']
        lw = session['linewidth']
        ls = session['linestyle']
        m = session['marker']
        ms = session['markersize']
        for paramform in fitform.params:
            paramform.species.choices = [(str(i), str(i)) for i, _ in enumerate(specs)] + [("None", "None")]

        if fitform.validate():
            category = "success"
            log.debug(f"Rxns: {rxns_sel},  Species: {specs_sel}")
            log.debug(fitform.data)
            # parse the data into a usable form
            orders = [form.order.data for form in fitform.params]
            poisons = [form.poison.data for form in fitform.params]
            excesses = [form.excess.data for form in fitform.params]
            param_specs = [form.species.data for form in fitform.params]
            conc_multipliers = [form.concs.data for form in fitform.params]
            session['param_specs'] = param_specs
            session['conc_multipliers'] =  conc_multipliers
            session['poisons'] = poisons

            totals = vh.get_sheet_totals(normtype, raw_data)
            norm_data = vh.shift_times(vh.normalize_columns(raw_data, totals), starts)
            # norm_data = vh.multiply_concs(norm_data, concs)
            select_data = vh.select_data(norm_data, reactions=rxns_sel, species=specs_sel)

            # Get the concentrations to normalize by
            concs = [[] for _ in select_data]

            for i, rxn in enumerate(select_data):
                for j, spec in enumerate(param_specs):
                    if spec == "None": # This means it is an excess reagent / catalyst
                        concs[i].append([conc_multipliers[j][i] - poisons[j] for _ in range(rxn.values.shape[0])])
                    else:
                        concs[i].append(list(rxn.iloc[:, j+1].values - poisons[j]))
            log.debug(concs)
            for i, rxn_concs in enumerate(concs):
                concs[i] = np.array(rxn_concs).T

            session['orders'] = np.array(orders)
            session['concs'] = concs
            new_plot, fig = plot_vtna(select_data, norm_time=True, concs=concs, orders=np.array(orders), marker=m,
                                      linestyle=ls, markersize=ms, linewidth=lw, guide_lines=guidelines, legend=legend)
            # save the filename and pickle the figure
            pickle.dump(fig, open(session['fig'], 'wb'))
            plt.close(fig)
            log.debug(f'Current Figures: {plt.get_fignums()}')
            fb = "Updated Manual VTNA Fit"
        else:
            fb = f"Update failed: {fitform.errors}"

        return make_response(jsonify(feedback=fb, rxns=rxns, specs=specs, category=category, new_plot=new_plot,
                             rxns_sel=rxns_sel, specs_sel=specs_sel), 200)

@app.route('/apply-style', methods=['POST'])
def style_data():
    styleform = StyleForm()

    if request.method == 'POST':
        result = ""
        category = "danger"
        starts = session['starts']
        raw_data = session['raw_data']
        rxns = session['rxns']
        normtype = session['normtype']
        rxns_sel = session['rxns_sel']
        specs_sel = session['specs_sel']
        specs = session['reactants']
        orders = session['orders']
        concs = session['concs']
        normtime = True if concs is not None else False

        session['legend'] = styleform.legend.data
        session['guidelines'] = styleform.guidelines.data
        session['linewidth'] = styleform.linewidth.data
        session['linestyle'] = styleform.linestyle.data
        session['marker'] = styleform.marker.data
        session['markersize'] = styleform.markersize.data

        if styleform.validate():
            category = "success"
            log.debug(styleform.data)

            # format the data for plotting
            totals = vh.get_sheet_totals(normtype, raw_data)
            norm_data = vh.shift_times(vh.normalize_columns(raw_data, totals), starts)
            select_data = vh.select_data(norm_data, reactions=rxns_sel, species=specs_sel)

            new_plot, fig = plot_vtna(select_data, norm_time=normtime, concs=concs, orders=orders, marker=session['marker'],
                                      linestyle=session['linestyle'], markersize=session['markersize'],
                                      linewidth=session['linewidth'], guide_lines=session['guidelines'],
                                      legend=session['legend'])
            # save the filename and pickle the figure
            pickle.dump(fig, open(session['fig'], 'wb'))
            plt.close(fig)
            log.debug(f'Current Figures: {plt.get_fignums()}')
            fb = "Updated Manual VTNA Fit"
        else:
            fb = f"Update failed: {fitform.errors}"

        return make_response(jsonify(feedback=fb, rxns=rxns, specs=specs, category=category, new_plot=new_plot,
                                     rxns_sel=rxns_sel, specs_sel=specs_sel), 200)


@app.route('/auto-fit', methods=['POST'])
def autofit_data():
    return '', 204


# @app.route('/format', methods=['POST'])
# def format_plot():
#     format_form = VTNAForm()
#     if request.method == 'POST' and format_form.validate():
#         log.debug("Submitted formatting form")
#         return '', 204
#     else:
#         for field, errors in format_form.errors.items():
#             for error in errors:
#                 log.debug(str(field) + ': ' + str(error))
#         return '', 204


@app.route('/download-vtna', methods=['POST'])
def download_vtna():
    log.debug('Download Initiated!')
    d_form = DVTNAForm()

    if request.method == 'POST' and d_form.validate():
        f_format = d_form.f_format.data
        log.debug(f"Save figure as {f_format}.")
        filename = secure_filename(f'vtna_plot.{f_format}')

        fig = pickle.load(open(session['fig'], 'rb'))
        img, mimetype = save_dfig(fig, f_format)
        plt.close(fig)
        img.seek(0)
        img = FileWrapper(img)
        response = make_response(Response(img, mimetype=mimetype, direct_passthrough=True))
        response.headers.set('Content-Disposition', 'attachment', filename=filename)
        return response
    else:
        log.debug("Not sending anything")
        return '', 204
