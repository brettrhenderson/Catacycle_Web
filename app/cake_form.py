from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, BooleanField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, InputRequired, ValidationError, optional
from flask_wtf.file import FileRequired, FileField
import re


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

class ContinuousAdditionForm(FlaskForm):
    """Field Enclosure for parameters of continuous addition of a reagent"""
    add_sol_conc = FloatField('Addition Solution Conc.', [InputRequired()], description="Concentration of reagent added.")
    add_cont_rate = FloatField('Rate of Addition', [InputRequired()], description="Rate of addition in moles_unit volume_unit^-1 time_unit^-1.")
    t_cont_rate = FloatField('After Time', [optional()], default=0.0, description="Time when addition began.")


class InstantaneousAdditionForm(FlaskForm):
    """Field Enclosure for parameters of continuous addition of a reagent"""
    add_sol_conc = FloatField('Addition Solution Conc.', [InputRequired()], description="Concentration of reagent added.")
    add_v_one_shot = FloatField('Volume Added', [InputRequired()], description="Volume of solution added in volume_unit.")
    t_one_shot = FloatField('At Time', [optional()], default=0.0, description="Time when addition occured.")


class SpeciesForm(FlaskForm):
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
    ord_val = FloatField('Est Order', [optional()], id='ord_val', default=1, description="Estimated species order")
    ord_min = FloatField('Min Order', [optional()], id='ord_min', default=0, description="Minimum species order search constraint")
    ord_max = FloatField('Max Order', [optional()], id='ord_max', default=2,
                         description="Maximum species order search constraint")
    pois_val = FloatField('Est Poisoning', [optional()], id='pois_val', default=0, description="Estimated species poisoning")
    pois_min = FloatField('Min Poisoning', [optional()], id='pois_min',
                          description="Minimum species poisoning search constraint")
    pois_max = FloatField('Max Poisoning', [optional()], id='ord_max',
                          description="Maximum species poisoning search constraint")
    cont_add = FieldList(FormField(ContinuousAdditionForm), min_entries=1)
    one_shot = FieldList(FormField(InstantaneousAdditionForm), min_entries=1)
    for_fitting = BooleanField("Use For Fitting", description="Use this species to perform CAKE fitting.")

    def format_r_ord(self):
        if self.ord_val.data is None:
            ord = self.ord_val.data
        elif self.ord_min.data is None or self.ord_max.data is None:
            ord = [self.ord_val.data]
        else:
            ord = [self.ord_val.data, self.ord_min.data, self.ord_max.data]
        return ord


class UploadForm(FlaskForm):
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
    t_init = FloatField("Simulation Start", description="Simulation start tike. Only used if sim==True")
    t_final = FloatField("Simulation End", description="Simulation end time. Only used if sim==True")
    t_interval = FloatField("Simulation Time Interval", description="Time interval for simulation run. Only used if sim==True")


class ReactionInformationForm(FlaskForm):
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


class DataManipulationForm(FlaskForm):
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


class CakeDownloadMultiForm(CakeFormMulti):
    # File Format Tab
    f_format = StringField('f_format', default='.svg')
    image_index = IntegerField('image_index', default=0)

