from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, SubmitField, FloatField, IntegerField, BooleanField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, InputRequired, ValidationError, optional
from flask_wtf.file import FileRequired, FileField
import re
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class FlaskRegexp(object):
    """
    Validates the field against a user provided regexp.

    :param regex:
        The regular expression string to use. Can also be a compiled regular
        expression pattern.
    :param flags:
        The regexp flags to use, for example re.IGNORECASE. Ignored if
        `regex` is not a string.
    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, regex, flags=0, message=None):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)
        self.regex = regex
        self.message = message

    def __call__(self, form, field, message=None):
        match = self.regex.match(field.data.filename or '')
        if not match:
            if message is None:
                if self.message is None:
                    message = field.gettext('Invalid input.')
                else:
                    message = self.message

            raise ValidationError(message)
        return match


class CakeForm(FlaskForm):
    xl = FileField('Select Data',
                   [FileRequired(), FlaskRegexp(r'^[a-zA-Z0-9\s_.\-\(\):]+\.xlsx$', flags=re.IGNORECASE,
                                                message="File must have .xslx extension.")],
                   description='Upload Reaction Data in Excel file format.',
                   id='excelUpload')
    sheet_name = StringField('Sheet Name', [InputRequired()], id='sheet_name', description="Name of sheet in Excel file, case sensitive",
                             default='Sheet1')
    t_col = IntegerField('Time Column', [InputRequired()], id='t_col', description="Integer index, 1 is the first column")
    r_col = IntegerField('Reactant Column', [optional()], id='r_col',
                         description="Integer index, 1 is the first column")
    p_col = IntegerField('Product Column', [optional()], id='p_col',
                         description="Integer index, 1 is the first column")
    fit_asp = SelectField('Fit Aspect', description="What trace to fit", id='fit_asp',
                          choices=[('r', 'Reactant'), ('p', 'Product'), ('rp', 'Reactant + Product')])
    scale_avg_num = IntegerField('Average Points', id='scale_avg_num', default=0,
                                 description="Number of data points from which to calculate r0 and p_end. Default 0 (no scaling).")
    stoich_r = IntegerField('Reactant Coefficient', [InputRequired()], id='stoich_r', description="Stoichiometric coefficient of reactant",
                            default=1)
    stoich_p = IntegerField('Product Coefficient', [InputRequired()], id='stoich_p', description="Stoichiometric coefficient of product",
                            default=1)
    r0 = FloatField('Starting Reactant Concentration', [optional()], id='r0', description="Initial reactant concentration")
    p0 = FloatField('Starting Product Concentration', [optional()], id='p0', description="Initial product concentration", default=0.0)
    p_end = FloatField('Final Product Concentration', [optional()], id='p_end', description="Final Product concentration")
    cat_sol_conc = FloatField('Catalyst Concentration', [InputRequired()], id='cat_sol_conc',
                              description='Concentration of the catalyst solution being added to the reaction')
    t_inj = FloatField('Time of Injection', [InputRequired()], id='t_inj',
                             description='Time at which catalyst injection began', default=0.0)
    inject_rate = FloatField('Injection Rate', [InputRequired()], id='inject_rate',
                             description='Rate of addition of catalyst solution to the reaction mixture')
    react_vol_init = FloatField('Initial Rxn Solution Volume', [InputRequired()], id='react_vol_init',
                                description='Initial volume of reactant solution to which catalyst is added')
    win = IntegerField('Smoothing Window', id='win', default=1, description="Number of points in smoothing window")
    inc = IntegerField('Interpolation Multiplier', id='inc',
                       description='Number of points to interpolate between measurements', default=1)

    k_est_val = FloatField('Est Rate Constant', [optional()], id='k_est_val', description="Estimated rate constant")
    k_est_min = FloatField('Min Rate Constant', [optional()], id='k_est_min',
                           description="Minimum rate constant search constraint")
    k_est_max = FloatField('Max Rate Constant', [optional()], id='k_est_max',
                           description="Maximum rate constant search constraint")

    r_ord_val = FloatField('Est Reactant Order', [optional()], id='r_ord_val', default=1, description="Estimated reactant order")
    r_ord_min = FloatField('Min Reactant Order', [optional()], id='r_ord_min', default=0,
                           description="Minimum reactant order search constraint")
    r_ord_max = FloatField('Max Reactant Order', [optional()], id='r_ord_max', default=2,
                           description="Maximum reactant order search constraint")

    cat_ord_val = FloatField('Est Catalyst Order', [optional()], id='c_ord_val', default=1, description="Estimated catalyst order")
    cat_ord_min = FloatField('Min Catalyst Order', [optional()], id='c_ord_min', default=0,
                             description="Minimum catalyst order search constraint")
    cat_ord_max = FloatField('Max Catalyst Order', [optional()], id='c_ord_max', default=2,
                             description="Maximum catalyst order search constraint")

    t0_est_val = FloatField('Est Start Time', [optional()], id='t0_est_val', description="Estimated reaction start time")
    t0_est_min = FloatField('Min Start Time', [optional()], id='t0_est_min',
                            description="Minimum start time search constraint")
    t0_est_max = FloatField('Max Start Time', [optional()], id='t0_est_max',
                            description="Maximum start time search constraint")

    submit = SubmitField('Fit', id='fit-submit')

    def format_k_est(self):
        if self.k_est_val.data is None:
            k_est = self.k_est_val.data
        elif self.k_est_min.data is None or self.k_est_max.data is None:
            k_est = [self.k_est_val.data]
        else:
            k_est = [self.k_est_val.data, self.k_est_min.data, self.k_est_max.data]
        return k_est

    def format_r_ord(self):
        if self.r_ord_val.data is None:
            r_ord = self.r_ord_val.data
        elif self.r_ord_min.data is None or self.r_ord_max.data is None:
            r_ord = [self.r_ord_val.data]
        else:
            r_ord = [self.r_ord_val.data, self.r_ord_min.data, self.r_ord_max.data]
        return r_ord

    def format_cat_ord(self):
        if self.cat_ord_val.data is None:
            cat_ord = self.cat_ord_val.data
        elif self.cat_ord_min.data is None or self.cat_ord_max.data is None:
            cat_ord = [self.cat_ord_val.data]
        else:
            cat_ord = [self.cat_ord_val.data, self.cat_ord_min.data, self.cat_ord_max.data]
        return cat_ord

    def format_t0_est(self):
        if self.t0_est_val.data is None:
            t0_est = self.t0_est_val.data
        elif self.t0_est_min.data is None or self.t0_est_max.data is None:
            t0_est = [self.t0_est_val.data]
        else:
            t0_est = [self.t0_est_val.data, self.t0_est_min.data, self.t0_est_max.data]
        return t0_est


class CakeDownloadForm(CakeForm):
    # File Format Tab
    f_format = StringField('f_format', default='.svg')
    image_index = IntegerField('image_index', default=0)


#################################################
# Modular Re-write for multiple-reactant fitting
#################################################

class ContinuousAdditionForm(Form):
    """Field Enclosure for parameters of continuous addition of a reagent"""
    add_sol_conc = FloatField('Addition Solution Conc.', [optional()], description="Concentration of reagent added.")
    add_cont_rate = FloatField('Rate of Addition', [optional()], description="Rate of addition in moles_unit volume_unit^-1 time_unit^-1.")
    t_cont_rate = FloatField('After Time', [optional()], default=0.0, description="Time when addition began.")


class InstantaneousAdditionForm(Form):
    """Field Enclosure for parameters of continuous addition of a reagent"""
    add_sol_conc = FloatField('Addition Solution Conc.', [optional()], description="Concentration of reagent added.")
    add_v_one_shot = FloatField('Volume Added', [optional()], description="Volume of solution added in volume_unit.")
    t_one_shot = FloatField('At Time', [optional()], default=0.0, description="Time when addition occured.")


class SpeciesForm(Form):
    """
    A form collecting all attributes of a species participating in a reaction.

    To be used as a FormField within a FieldList of species for a given reaction.

    Attributes
    ----------
    col : :obj:`wtforms.IntegerField`
        Column in excel sheet to use for this reaction species.
    spec_type: :obj:`wtforms.SelectField`
        The type of species (reactant, product, or catalyst)
    stoich : :obj:`wtforms.IntegerField`
        Stoichiometric coefficient for this reaction species. Default 1.
    mol_init : :obj:`wtforms.FloatField`, optional
        Initial amount of species in moles. If not given, excel values will be assumed to be given in moles.
    mol_end : :obj:`wtforms.FloatField`, optional
        Final amount of species in moles. If not given, excel values will be assumed to be given in moles.

    """
    col = IntegerField('Column', [InputRequired()], description="Integer index, 1 is the first column.")
    spec_name = StringField('Species Name', [optional()], description="Name of species.")
    spec_type = SelectField('Species Type', [InputRequired()], description="Type of Species (reactant, product, catalyst).",
                            choices=[('r', 'Reactant'), ('p', 'Product'), ('c', 'Catalyst')])
    stoich = IntegerField('Stoichiometry', [InputRequired()], description="Stoichiometric coefficient of species.", default=1)
    mol_init = FloatField('Initial Moles', [optional()], description="Initial amount in moles.")
    mol_end = FloatField('Final Moles', [optional()], description="Final amount in moles")
    ord_val = FloatField('Est Order', [optional()], default=1, description="Estimated species order")
    ord_min = FloatField('Min Order', [optional()], default=0, description="Minimum species order search constraint")
    ord_max = FloatField('Max Order', [optional()], default=2,
                         description="Maximum species order search constraint")
    pois_val = FloatField('Est Poisoning', [optional()], default=0, description="Estimated species poisoning")
    pois_min = FloatField('Min Poisoning', [optional()],
                          description="Minimum species poisoning search constraint")
    pois_max = FloatField('Max Poisoning', [optional()],
                          description="Maximum species poisoning search constraint")
    cont_add = FieldList(FormField(ContinuousAdditionForm), min_entries=0)
    one_shot = FieldList(FormField(InstantaneousAdditionForm), min_entries=0)
    for_fitting = BooleanField("Use For Fitting", description="Use this species to perform CAKE fitting. Must specify column to enable")


def format_ord(data_dict):
    if data_dict['ord_val'] is None:
        order = data_dict['ord_val']
    elif data_dict['ord_min'] is None or data_dict['ord_max'] is None:
        order = (data_dict['ord_val'])
    else:
        order = (data_dict['ord_val'], data_dict['ord_min'], data_dict['ord_max'])
    return order


def format_pois(data_dict):
    if data_dict['pois_val'] is None:
        pois = data_dict['pois_val']
    elif data_dict['pois_min'] is None or data_dict['pois_max'] is None:
        pois = (data_dict['pois_val'])
    else:
        pois = (data_dict['pois_val'], data_dict['pois_min'], data_dict['pois_max'])
    return pois


class UploadForm(Form):
    """
    To be used as a FormField within a the overall reaction form.

    Attributes
    ----------
    xl : :obj:`flask_wtf.file.FileField`
        Excel file containing reaction data for CAKE analysis
    sheet_name : :obj:`wtforms.StringField`
        Name of the sheet in excel file containing desired reaction data.
    t_col: :obj:`wtforms.IntegerField`
        Column in excel sheet to use for the time variable. 1 is the first column.
    sim: :obj: `wtforms.BooleanField`
        Whether the reaction is to be merely simulated or actually analyzed from Excel data
    """
    xl = FileField('Select Data',
                   [FileRequired(), FlaskRegexp(r'^[a-zA-Z0-9\s_.\-\(\):]+\.xlsx$', flags=re.IGNORECASE,
                                                message="File must have .xslx extension.")],
                   description='Upload Reaction Data in Excel file format.',
                   id='excelUpload')
    sheet_name = StringField('Sheet Name', [InputRequired()], id='sheet_name',
                             description="Name of sheet in Excel file, case sensitive",
                             default='Sheet1')
    t_col = IntegerField('Time Column', [InputRequired()], id='t_col',
                         description="Integer index, 1 is the first column")
    sim = BooleanField("Simulate Reaction", id="sim-box", description="Simulate without reading actual reaction data from Excel.")
    t_init = FloatField("Simulation Start", [optional()], description="Simulation start tike. Only used if sim==True")
    t_final = FloatField("Simulation End", [optional()], description="Simulation end time. Only used if sim==True")
    t_interval = FloatField("Simulation Time Interval", [optional()], description="Time interval for simulation run. Only used if sim==True")


class ReactionInformationForm(Form):
    """
    Contains All of the information about a reaction needed to perform CAKE analysis

    """
    react_vol_init = FloatField('Initial Reaction Volume', [InputRequired()], description="Initial volume of reactants.")

    k_est_val = FloatField('Est Rate Constant', [optional()], id='k_est_val', description="Estimated rate constant")
    k_est_min = FloatField('Min Rate Constant', [optional()], id='k_est_min',
                           description="Minimum rate constant search constraint")
    k_est_max = FloatField('Max Rate Constant', [optional()], id='k_est_max',
                           description="Maximum rate constant search constraint")
    species = FieldList(FormField(SpeciesForm), min_entries=1)

    def format_k_est(self):
        if self.k_est_val.data is None:
            k_est = self.k_est_val.data
        elif self.k_est_min.data is None or self.k_est_max.data is None:
            k_est = [self.k_est_val.data]
        else:
            k_est = [self.k_est_val.data, self.k_est_min.data, self.k_est_max.data]
        return k_est


class DataManipulationForm(Form):
    """
    Contains all parameters for smoothing and otherwise manipulating reaction data
    """
    scale_avg_num = IntegerField('Average Points', id='scale_avg_num', default=0,
                                 description="Number of data points from which to calculate r0 and p_end. Default 0 (no scaling).")
    win = IntegerField('Smoothing Window', id='win', default=1, description="Number of points in smoothing window")
    inc = IntegerField('Interpolation Multiplier', id='inc',
                       description='Number of points to interpolate between measurements', default=1)


class CakeFormMulti(FlaskForm):
    """
    A form collecting all attributes of a species participating in a reaction.

    To be used as a FormField within a FieldList of species for a given reaction.

    Attributes
    ----------
    xl : :obj:`flask_wtf.file.FileField`
        Excel file containing reaction data for CAKE analysis
    sheet_name : :obj:`wtforms.StringField`
        Name of the sheet in excel file containing desired reaction data.
    t_col: :obj:`wtforms.IntegerField`
        Column in excel sheet to use for the time variable. 1 is the first column.
    """

    upload = FormField(UploadForm)
    rxn_info = FormField(ReactionInformationForm)
    data_manip = FormField(DataManipulationForm)

    submit = SubmitField('Fit', id='fit-submit')

    # TODO: Data Formatters to Prepare data in the proper structures for cake_fitting.py
    def prepare_data(self):
        data = self.data
        react_vol_init = data['rxn_info']['react_vol_init']

        # reset column indices to 1-indexed
        t_col = None
        if data['upload']['t_col']:
            t_col = data['upload']['t_col'] - 1

        # go through each species in data
        spec_name, spec_type, stoich, mol0, mol_end, add_sol_conc, add_cont_rate = [], [], [], [], [], [], []
        add_one_shot, t_one_shot, t_cont, col, ord_lim, pois_lim, fit_asp = [], [], [], [], [], [], []
        for i, spec in enumerate(data['rxn_info']['species']):
            if spec['spec_name']:
                spec_name.append(spec['spec_name'])
            else:
                spec_name.append(f"Species {i + 1}")
            spec_type.append(spec['spec_type'])
            stoich.append(spec['stoich'])
            mol0.append(spec['mol_init'])
            mol_end.append(spec['mol_end'])
            col.append(spec['col'])
            ord_lim.append(format_ord(spec))
            pois_lim.append(format_pois(spec))

            # fit aspect
            if spec['for_fitting']:
                fit_asp.append('y')
            else:
                fit_asp.append('n')

            # Additions
            if not len(spec['cont_add']) and not len(spec['one_shot']):
                add_sol_conc.append(None)
                add_cont_rate.append(None)
                t_cont.append(None)
                add_one_shot.append(None)
                t_one_shot.append(None)
            else:
                if not len(spec['cont_add']):
                    add_cont_rate.append(None)
                    t_cont.append(None)
                else:
                    conc = spec['cont_add']['add_sol_conc']
                    rates = []
                    times = []
                    for addition in spec['cont_add']:
                        rates.append(addition['add_cont_rate'])
                        times.append(addition['t_cont_rate'])
                    add_cont_rate.append(tuple(rates))
                    t_cont.append(tuple(times))

                if not len(spec['one_shot']):
                    add_one_shot.append(None)
                    t_one_shot.append(None)
                else:
                    conc = spec['cont_add']['add_sol_conc']
                    one_shot_amts = []
                    times = []
                    for addition in spec['one_shot']:
                        one_shot_amts.append(addition['add_v_one_shot'])
                        times.append(addition['t_one_shot'])
                    add_one_shot.append(tuple(one_shot_amts))
                    t_one_shot.append(tuple(times))
                add_sol_conc.append(conc)

        data_dict = {"xl": data['upload']['xl'],
                     "sheet_name": data['upload']['sheet_name'],
                     "spec_name": spec_name,
                     "spec_type": spec_type,
                     "react_vol_init": react_vol_init,
                     "stoich": stoich,
                     "mol0": mol0,
                     "mol_end": mol_end,
                     "add_sol_conc": add_sol_conc,
                     "add_cont_rate": add_cont_rate,
                     "t_cont": t_cont,
                     "add_one_shot": add_one_shot,
                     "t_one_shot": t_one_shot,
                     "t_col": t_col,
                     "col": col,
                     "ord_lim": ord_lim,
                     "pois_lim": pois_lim,
                     "fit_asp": fit_asp}

        return data_dict


class CakeDownloadMultiForm(CakeFormMulti):
    # File Format Tab
    f_format = StringField('f_format', default='.svg')
    image_index = IntegerField('image_index', default=0)

