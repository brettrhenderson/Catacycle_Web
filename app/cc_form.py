from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, SubmitField, FloatField, IntegerField, BooleanField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, InputRequired, ValidationError, optional
from flask_wtf.file import FileRequired, FileField
import re
import logging

from continuous_calibration.fitting.gen_eqs import fit_eq_custom

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
    add_sol_conc = FloatField('Addition Solution Conc', description='Concentration of reagent added in moles_unit volume_unit⁻¹')
    add_cont_rate = FloatField('Rate of Addition', description='Rate of addition in moles_unit volume_unit⁻¹ time_unit⁻¹')
    t_cont_rate = FloatField('After Time', default=0.0, description='Time when addition began in time_unit')


class DiscreteAdditionForm(Form):
    """Field Enclosure for parameters of continuous addition of a reagent"""
    add_sol_conc = FloatField('Addition Solution Conc', description='Concentration of reagent added in moles_unit volume_unit⁻¹')
    add_v_one_shot = FloatField('Volume Added', description='Volume of solution added in volume_unit')
    t_one_shot = FloatField('At Time', default=0.0, description='Time when addition occurred in time_unit')


class SpeciesForm(Form):
    """
    A form collecting all attributes of a species participating in a reaction.

    To be used as a FormField within a FieldList of species for a given reaction.

    Attributes
    ----------
    gen_col : :obj:`wtforms.IntegerField`
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
    spec_name = StringField('Species Name', description='Name of species')
    mol0 = FloatField('Initial Moles', description='Initial amount in mole_unit', default=0)
    gen_col = StringField('Generation Column', description='Input column name or index, where 1 is the first column')
    apply_col = StringField('Application Column', description='Input column name or index, where 1 is the first column')
    cont_add = FieldList(FormField(ContinuousAdditionForm), min_entries=0)
    one_shot = FieldList(FormField(DiscreteAdditionForm), min_entries=0)

class UploadForm(Form):
    """
    To be used as a FormField within the overall reaction form.

    Attributes
    ----------
    gen_xl : :obj:`flask_wtf.file.FileField`
        Excel file containing reaction data for CAKE analysis
    gen_sheet_name : :obj:`wtforms.StringField`
        Name of the sheet in Excel file containing desired reaction data.
    gen_t_col: :obj:`wtforms.IntegerField`
        Column in Excel sheet to use for the time variable. 1 is the first column.
    """
    gen_xl = FileField('Select Calibration Data',
                       [InputRequired(), FlaskRegexp(r'^[a-zA-Z0-9\s_.\-\(\):]+\.xlsx$', flags=re.IGNORECASE,
                                                message='File must have .xlsx extension')],
                       description='Upload calibration data in Excel file format',
                       id='gen_xl_upload')
    gen_sheet_name = StringField('Sheet Name', id='gen_sheet_name',
                                 description='Name of sheet in Excel file, case sensitive', default='Sheet1')
    gen_t_col = StringField('Time Column', id='gen_t_col',
                            description='Time column name or index, where 1 is the first column. Time column must be in time_unit')

    apply = BooleanField('Apply Calibration', id='apply-box', description='Apply calibration to experimental data', default=False)

    apply_xl = FileField('Select Experimental Data',
                       [optional(), FlaskRegexp(r'^[a-zA-Z0-9\s_.\-\(\):]+\.xlsx$', flags=re.IGNORECASE,
                                                message='File must have .xlsx extension')],
                         description='Upload experimental data requiring calibration in Excel file format',
                         id='apply_xl_upload')
    apply_sheet_name = StringField('Sheet Name', id='apply_sheet_name',
                                   description='Name of sheet in Excel file, case sensitive', default='Sheet1')
    apply_t_col = StringField('Time Column', id='apply_t_col',
                              description='Time column name or index, where 1 is the first column. Time column must be in time_unit')

class SystemForm(Form):
    """
    Contains parameters needed to generate the calibration
    """
    vol0 = FloatField('Initial Solution Volume', [InputRequired()], description='Initial volume of monitored solution')
    sub_cont_rate = FloatField('Continuous Volume Loss Rate', [optional()],
                               description='Rate of continuous solution loss in volume_unit time_unit⁻¹', default=0.0)

    species = FieldList(FormField(SpeciesForm), min_entries=1)

class FitForm(Form):
    """
    Contains parameters for fitting calibration data
    """
    path_length = FloatField('Path Length', [optional()], id='path_length', description='Length of light path in absorption spectroscopy if desired')

    fit_eq = SelectField('Fit Equation', id='fit_eq', description='Equation type to fit data with',
                         choices=[('Linear', 'Linear'), ('Logarithm', 'Logarithm'), ('Exponential', 'Exponential'), ('Tangent', 'Tangent'), ('Michaelis-Menten', 'Michaelis-Menten'), ('Langmuir', 'Langmuir'), ('None', 'None')], default='None')
    intercept = BooleanField('Fit Intercept', id='intercept-box', description='Fit data with intercept', default=False)

    lof = BooleanField('Fit Limit of Fitting', id='lof-box', description='Fit data with equation until no longer valid', default=False)
    lof_test = SelectField('Test', description='Algorithm for estimating limit of fitting', id='lof_test',
                           choices=[('RMSE', 'RMSE'), ('MAE', 'MAE'), ('R2', 'R2'), ('Runs', 'Runs'), ('Rainbow', 'Rainbow'), ('Harvey-Collier', 'Harvey-Collier'), ('Shapiro-Wilk', 'Shapiro-Wilk')])
    lof_method = SelectField('Selection', description='Selection criterion for estimating limit of fitting', id='lof_method',
                             choices=[('min', 'min'), ('max', 'max'), ('first', 'first'), ('last', 'last')], default='min')
    p_thresh = FloatField('Threshold', id='p_thresh', description='p-value threshold for estimating limit of fitting', default=0.05)

    smooth_eq = SelectField('Smoothing Equation', id='smooth_eq-box', description='Fit data with a smoothed line',
                            choices=[('monotonic', 'Monotonic GAM'), ('concave', 'Concave GAM'), ('Savitsky-Golay', 'Savitsky-Golay'), ('None', 'None')], default='concave')
    sg_win = IntegerField('Window', id='sg_win', description='Number of data points to use for Savitsky-Golay smoothing', default=11)

    lod_stds = FloatField('Limit of Detection Standard Deviations', id='lod_stds', description='Number of blank standard deviations from which to estimate limit of detection', default=3)


class ManipulationForm(Form):
    """
    Contains parameters for manipulating calibration data
    """
    breakpoint_lim = FloatField('Breakpoint Time Limit', id='breakpoint',
                       description='Additional time in which continuous additions may have occurred', default=0.0)
    diffusion_delay = FloatField('Diffusion Delay', id='diffusion',
                       description='Additional time in which it takes for discrete addition diffusions to occur', default=0.0)
    zero = BooleanField('Zero', id='zero-box', description='Set minimum intensity to zero', default=False)
    win = IntegerField('Smoothing Window', id='win', description='Number of points in smoothing window', default=1)
    inc = IntegerField('Interpolation Multiplier', id='inc',
                       description='Number of points to interpolate between measurements', default=1)


class CCForm(FlaskForm):
    """
    A form collecting all attributes of a species participating in a reaction.

    To be used as a FormField within a FieldList of species for a given reaction.

    Attributes
    ----------
    gen_xl : :obj:`flask_wtf.file.FileField`
        Excel file containing reaction data for CAKE analysis
    gen_sheet_name : :obj:`wtforms.StringField`
        Name of the sheet in excel file containing desired reaction data.
    gen_t_col: :obj:`wtforms.IntegerField`
        Column in excel sheet to use for the time variable. 1 is the first column.
    """

    upload = FormField(UploadForm)
    system = FormField(SystemForm)
    fit = FormField(FitForm)
    manip = FormField(ManipulationForm)

    submit = SubmitField('Calibrate', id='calib-submit')

    # TODO: Data Formatters to Prepare data in the proper structures for gen.py
    def prepare_data(self):
        data = self.data

        # reset column indices to 1-indexed
        try:
            gen_t_col = int(data['upload']['gen_t_col']) - 1
        except:
            gen_t_col = data['upload']['gen_t_col']
        if data['upload']['apply']:
            apply_xl = data['upload']['apply_xl']
            apply_sheet_name = data['upload']['apply_sheet_name']
            if data['upload']['apply_t_col']:
                try:
                    apply_t_col = int(data['upload']['apply_t_col']) - 1
                except:
                    apply_t_col = data['upload']['apply_t_col']
            else:
                apply_t_col = data['upload']['apply_t_col']
        else:
            apply_xl, apply_sheet_name, apply_t_col, apply_col = None, None, None, None

        # go through each species in data
        spec_name, mol0, add_sol_conc, add_cont_rate = [], [], [], []
        add_one_shot, t_one_shot, t_cont, gen_col, apply_col = [], [], [], [], []
        for i, spec in enumerate(data['system']['species']):
            if spec['spec_name']:
                spec_name.append(spec['spec_name'])
            else:
                spec_name.append(f"Species {i + 1}")
            mol0.append(spec['mol0'])
            try:
                gen_col.append(int(spec['gen_col']) - 1)
            except:
                gen_col.append(spec['gen_col'])
            if data['upload']['apply'] and spec['apply_col']:
                try:
                    apply_col.append(int(spec['apply_col']) - 1)
                except:
                    apply_col.append(spec['apply_col'])
            else:
                apply_col.append(spec['apply_col'])

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
                    add_cont_rate.append(rates)
                    t_cont.append(times)

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
                    add_one_shot.append(vols)
                    t_one_shot.append(times)
                add_sol_conc.append(conc)

        #Fits
        if 'None' in data['fit']['fit_eq']:
            fit_eq = None
        else:
            fit_eq = data['fit']['fit_eq']
        if data['fit']['lof']:
            lof_test = data['fit']['lof_test']
            lof_method = data['fit']['lof_method']
            p_thresh = data['fit']['p_thresh']
        else:
            lof_test, lof_method, p_thresh = None, None, None
        if 'None' in data['fit']['smooth_eq']:
            smooth_eq = None
        else:
            smooth_eq = data['fit']['smooth_eq']

        dict = {'gen_xl': data['upload']['gen_xl'],
                'gen_sheet_name': data['upload']['gen_sheet_name'],
                'gen_t_col': gen_t_col,
                'vol0': data['system']['vol0'],
                'sub_cont_rate': data['system']['sub_cont_rate'],
                'spec_name': spec_name,
                'mol0': mol0,
                'gen_col': gen_col,
                'add_sol_conc': add_sol_conc,
                'add_cont_rate': add_cont_rate,
                't_cont': t_cont,
                'add_one_shot': add_one_shot,
                't_one_shot': t_one_shot,
                'fit_eq': fit_eq,
                'intercept': data['fit']['intercept'],
                'path_length': data['fit']['path_length'],
                'lof_test': lof_test,
                'lof_method': lof_method,
                'p_thresh': p_thresh,
                'smooth_eq': smooth_eq,
                'sg_win': data['fit']['sg_win'],
                'lod_stds': data['fit']['lod_stds'],
                'breakpoint_lim': data['manip']['breakpoint_lim'],
                'diffusion_delay': data['manip']['diffusion_delay'],
                'zero': data['manip']['zero'],
                'win': data['manip']['win'],
                'inc': data['manip']['inc'],
                'apply_xl': apply_xl,
                'apply_sheet_name': apply_sheet_name,
                'apply_t_col': apply_t_col,
                'apply_col': apply_col}

        return dict


class CCDownloadForm(CCForm):
    # File Format Tab
    f_format = StringField('f_format', default='.svg')
    image_index = IntegerField('image_index', default=0)
