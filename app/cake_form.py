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
                    message = field.gettext('Invalid input')
                else:
                    message = self.message

            raise ValidationError(message)
        return match


class ContinuousAdditionForm(Form):
    """Field Enclosure for parameters of continuous addition of a reagent"""
    add_sol_conc = FloatField('Addition Solution Conc', [optional()], description='Concentration of reagent added')
    add_cont_rate = FloatField('Rate of Addition', [optional()], description='Rate of addition in moles_unit volume_unit^-1 time_unit^-1')
    t_cont_rate = FloatField('After Time', [optional()], default=0.0, description='Time when addition began')


class DiscreteAdditionForm(Form):
    """Field Enclosure for parameters of discrete addition of a reagent"""
    add_sol_conc = FloatField('Addition Solution Conc', [optional()], description='Concentration of reagent added')
    add_v_one_shot = FloatField('Volume Added', [optional()], description='Volume of solution added in volume_unit')
    t_one_shot = FloatField('At Time', [optional()], default=0.0, description='Time when addition occurred')


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
    mol0 : :obj:`wtforms.FloatField`, optional
        Initial amount of species in moles. If not given, excel values will be assumed to be given in moles.
    mol_end : :obj:`wtforms.FloatField`, optional
        Final amount of species in moles. If not given, excel values will be assumed to be given in moles.

    """
    spec_name = StringField('Species Name', [optional()], description='Name of species')
    spec_type = SelectField('Species Type', [InputRequired()], description='Type of Species (reactant, product, catalyst)',
                            choices=[('r', 'Reactant'), ('p', 'Product'), ('c', 'Catalyst')])
    stoich = IntegerField('Stoichiometry', [InputRequired()], description='Stoichiometric coefficient of species', default=1)
    mol0 = FloatField('Initial Moles', [optional()], description='Initial amount in mole_unit')
    mol_end = FloatField('Final Moles', [optional()], description='Final amount in mole_unit')
    col = IntegerField('Column', [optional()], description='Integer index, 1 is the first column')
    ord_val = FloatField('Est Order', [optional()], default=1, description='Estimated species order')
    ord_min = FloatField('Min Order', [optional()], default=0, description='Minimum species order search constraint')
    ord_max = FloatField('Max Order', [optional()], default=2,
                         description='Maximum species order search constraint')
    pois_val = FloatField('Est Poisoning', [optional()], default=0, description='Estimated species poisoning in mole_unit')
    pois_min = FloatField('Min Poisoning', [optional()],
                          description='Minimum species poisoning search constraint in mole_unit')
    pois_max = FloatField('Max Poisoning', [optional()],
                          description='Maximum species poisoning search constraint in mole_unit')
    cont_add = FieldList(FormField(ContinuousAdditionForm), min_entries=0)
    one_shot = FieldList(FormField(DiscreteAdditionForm), min_entries=0)
    for_fitting = BooleanField('Use For Fitting', description='Use this species to perform CAKE fitting. Must specify column to enable')


def format_ord(data_dict, sim=False):
    if sim:
        order = data_dict['ord_val']
    elif data_dict['ord_val'] is None:
        order = data_dict['ord_val']
    elif data_dict['ord_min'] is None or data_dict['ord_max'] is None:
        order = data_dict['ord_val']
    else:
        order = (data_dict['ord_val'], data_dict['ord_min'], data_dict['ord_max'])
    return order


def format_pois(data_dict, sim=False):
    if sim:
        pois = data_dict['pois_val']
    elif data_dict['pois_val'] is None:
        pois = data_dict['pois_val']
    elif data_dict['pois_min'] is None or data_dict['pois_max'] is None:
        pois = data_dict['pois_val']
    else:
        pois = (data_dict['pois_val'], data_dict['pois_min'], data_dict['pois_max'])
    return pois


class DiscreteSubtractionForm(Form):
    """Field Enclosure for parameters of discrete subtraction of a reagent"""
    sub_aliq = FloatField('Volume Removed', [optional()], description='Volume of solution removed in volume_unit')
    t_aliq = FloatField('At Time', [optional()], default=0.0, description='Time when removal occurred in time_unit')


class UploadForm(Form):
    """
    To be used as a FormField within the overall reaction form.

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
                   [optional(), FlaskRegexp(r'^[a-zA-Z0-9\s_.\-\(\):]+\.xlsx$', flags=re.IGNORECASE,
                                                message='File must have .xslx extension')],
                   description='Upload Reaction Data in Excel file format',
                   id='excelUpload')
    sheet_name = StringField('Sheet Name', [optional()], id='sheet_name',
                             description='Name of sheet in Excel file, case sensitive',
                             default='Sheet1')
    t_col = IntegerField('Time Column', [optional()], id='t_col',
                         description='Integer index, 1 is the first column. Time column must be in time_unit')
    sim = BooleanField('Simulate Reaction', id='sim-box', description='Simulate without reading experimental data from Excel')
    t0 = FloatField('Simulation Start', [optional()], default=0.0, description='Simulation start time in time_unit')
    t_end = FloatField('Simulation End', [optional()], description='Simulation end time in time_unit')
    t_int = FloatField('Simulation Time Interval', [optional()], description='Time interval for simulation run in time_unit')


class SystemForm(Form):
    """
    Contains all the information about a reaction needed to perform CAKE analysis
    """
    vol0 = FloatField('Initial Reaction Volume', [InputRequired()], description='Initial volume of reactants in volume_unit')
    sub_cont_rate = FloatField('Continuous Volume Loss Rate', [optional()], default=0.0,
                               description='Rate of continuous solution loss in volume_unit time_unit⁻¹')

    k_est_val = FloatField('Est Rate Constant', [optional()], id='k_est_val', description='Estimated rate constant')
    k_est_min = FloatField('Min Rate Constant', [optional()], id='k_est_min',
                           description='Minimum rate constant search constraint')
    k_est_max = FloatField('Max Rate Constant', [optional()], id='k_est_max',
                           description='Maximum rate constant search constraint')
    k2_est_val = FloatField('Est Second Constant', [optional()], id='k2_est_val', description='Estimated constant')
    k2_est_min = FloatField('Min Second Constant', [optional()], id='k2_est_min',
                           description='Minimum constant search constraint')
    k2_est_max = FloatField('Max Second Constant', [optional()], id='k2_est_max',
                           description='Maximum constant search constraint')
    species = FieldList(FormField(SpeciesForm), min_entries=1)

    t_cont_sub = FloatField('After Time', [optional()], id='t_cont_sub', default=0.0, description='Time when removal began in time_unit')
    aliq = FieldList(FormField(DiscreteSubtractionForm), min_entries=0)

    temp0 = FloatField('Initial Temperature', [optional()], default=293.15, description='Initial temperature in K')
    temp_cont = FloatField('Temperature Gradient', [optional()], default=0.0, description='Rate of temperature change in K time_unit⁻¹')
    t_temp = FloatField('At Time', [optional()], default=0.0, description='Time when gradient began in time_unit')
    temp_col = IntegerField('Temperature Column', [optional()], description='Integer index, 1 is the first column. Temperature column must be in K')

    def format_k_est(self, rate_eq_type='standard'):
        if self.k_est_min.data is None or self.k_est_max.data is None:
            k_est = [self.k_est_val.data]
        else:
            k_est = [self.k_est_val.data, self.k_est_min.data, self.k_est_max.data]
        if 'standard' not in rate_eq_type.lower():
            if self.k2_est_min.data is None or self.k2_est_max.data is None:
                k_est.append(self.k2_est_val.data)
            else:
                k_est.append([self.k2_est_val.data, self.k2_est_min.data, self.k2_est_max.data])
        return k_est


class FitForm(Form):
    """
    Contains all the parameters for rate equation
    """
    rate_eq_type = SelectField('Rate Equation', id='rate_eq', choices=[('standard', 'Standard'),
                              ('Arrhenius', 'Arrhenius'), ('Eyring', 'Eyring'),
                              ('Michaelis-Menten', 'Michaelis-Menten')], default='Standard',
                               description='Equation type for calculating reaction rate')
    rate_method = SelectField('Rate Algorithm', id='rate_eq', choices=[('RK45', 'RK45'), ('RK23', 'RK23'),
                             ('DOP853', 'DOP853'), ('Radau', 'Radau'), ('BDF', 'BDF'), ('LSODA', 'LSODA')],
                              default='Radau', description='Algorithm for caclulating reaction rate')
    rtol = FloatField('Relative Tolerance', id='rtol', default=1E-6,
                      description='Controls number of correct digits')
    atol = FloatField('Absolute Tolerance', id='atol', default=1E-9,
                       description='Controls number of correct decimal places')


class DataManipulationForm(Form):
    """
    Contains all parameters for manipulating reaction data
    """
    scale_avg_num = IntegerField('Average Points', id='scale_avg_num', default=0,
                                 description='Number of data points from which to calculate r0 and p_end. Default 0 (no scaling)')
    win = IntegerField('Smoothing Window', id='win', description='Number of points in smoothing window', default=1)
    inc = FloatField('Interpolation Multiplier', id='inc', default=1,
                       description='Fraction of points for fitting. Values < 1 use a fraction of experimental data. Values > 1 interpolate between data')
    rand_fac = FloatField('Noise Addition', id='rand_fac', default=0,
                          description='Noise as fraction of the most intense species maximum')


class CakeForm(FlaskForm):
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
    system = FormField(SystemForm)
    fit = FormField(FitForm)
    manip = FormField(DataManipulationForm)

    submit = SubmitField('Fit', id='fit-submit')

    # TODO: Data Formatters to Prepare data in the proper structures for cake_fitting.py
    def prepare_data(self, sim=False):
        data = self.data

        k_lim = self.system.format_k_est(rate_eq_type=data['fit']['rate_eq_type'])

        # reset column indices to 1-indexed
        t_col = None
        if data['upload']['t_col']:
            t_col = data['upload']['t_col'] - 1

        # go through each species in data
        spec_name, spec_type, stoich, mol0, mol_end, add_sol_conc, add_cont_rate = [], [], [], [], [], [], []
        add_one_shot, t_one_shot, t_cont, col, ord_lim, pois_lim, fit_asp = [], [], [], [], [], [], []
        for i, spec in enumerate(data['system']['species']):
            if spec['spec_name']:
                spec_name.append(spec['spec_name'])
            else:
                spec_name.append(f"Species {i + 1}")
            spec_type.append(spec['spec_type'])
            stoich.append(spec['stoich'])
            mol0.append(spec['mol0'])
            mol_end.append(spec['mol_end'])
            if spec['col'] is not None:
                col.append(spec['col'] - 1)
            else:
                col.append(spec['col'])
            ord_lim.append(format_ord(spec, sim))
            pois_lim.append(format_pois(spec, sim))

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
                    conc = spec['cont_add'][0]['add_sol_conc']
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
                    log.debug(spec['one_shot'])
                    conc = spec['one_shot'][0]['add_sol_conc']
                    vols = []
                    times = []
                    for addition in spec['one_shot']:
                        vols.append(addition['add_v_one_shot'])
                        times.append(addition['t_one_shot'])
                    add_one_shot.append(tuple(vols))
                    t_one_shot.append(tuple(times))
                add_sol_conc.append(conc)

        # Subtractions
        sub_aliq, t_aliq = [], []
        if not len(data['system']['aliq']):
            sub_aliq.append(None)
            t_aliq.append(None)
        else:
            for subtraction in data['system']['aliq']:
                sub_aliq.append(subtraction['sub_aliq'])
                t_aliq.append(subtraction['t_aliq'])

        dict = {'sim': data['upload']['sim'],
                't': (data['upload']['t0'], data['upload']['t_end'], data['upload']['t_int']),
                'xl': data['upload']['xl'],
                'sheet_name': data['upload']['sheet_name'],
                'spec_name': spec_name,
                'spec_type': spec_type,
                'vol0': data['system']['vol0'],
                'stoich': stoich,
                'mol0': mol0,
                'mol_end': mol_end,
                'add_sol_conc': add_sol_conc,
                'add_cont_rate': add_cont_rate,
                't_cont': t_cont,
                'add_one_shot': add_one_shot,
                't_one_shot': t_one_shot,
                't_col': t_col,
                'col': col,
                'k_lim': k_lim,
                'ord_lim': ord_lim,
                'pois_lim': pois_lim,
                'fit_asp': fit_asp,
                'sub_cont_rate': data['system']['sub_cont_rate'],
                'sub_aliq': sub_aliq,
                't_aliq': t_aliq,
                'temp0': data['system']['temp0'],
                'temp_cont': data['system']['temp_cont'],
                't_temp': data['system']['t_temp'],
                'temp_col': data['system']['temp_col'],
                'rate_eq_type': data['fit']['rate_eq_type'],
                'rate_method': data['fit']['rate_method'],
                'rtol': data['fit']['rtol'],
                'atol': data['fit']['atol'],
                'scale_avg_num': data['manip']['scale_avg_num'],
                'win': data['manip']['win'],
                'inc': data['manip']['inc'],
                'rand_fac': data['manip']['rand_fac'],
                'tic_col': None,
                'time_unit': None,
                'conc_unit': None}
        return dict


class CakeDownloadForm(CakeForm):
    # File Format Tab
    f_format = StringField('f_format', default='.svg')
    image_index = IntegerField('image_index', default=0)
