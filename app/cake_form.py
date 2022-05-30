from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, BooleanField, SelectField
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
    tic_col = IntegerField('Total Ion Count Column', [optional()], id='tic_col',
                           description="Integer index, 1 is the first column")
    r_col = IntegerField('Reactant Column', [optional()], id='r_col',
                         description="Integer index, 1 is the first column")
    p_col = IntegerField('Product Column', [optional()], id='p_col',
                         description="Integer index, 1 is the first column")
    fit_asp = SelectField('Fit Aspect', description="What trace to fit", id='fit_asp',
                          choices=[('r', 'Reactant'), ('p', 'Product'), ('rp', 'Reactant + Product')])
    scale_avg_num = IntegerField('Average Points', id='scale_avg_num', default=5,
                                 description="Number of points to average for calculating r0 and p_end")
    stoich_r = IntegerField('Reactant Coefficient', [InputRequired()], id='stoich_r', description="Stoichiometric coefficient of reactant",
                            default=1)
    stoich_p = IntegerField('Product Coefficient', [InputRequired()], id='stoich_p', description="Stoichiometric coefficient of product",
                            default=1)
    r0 = FloatField('Starting Reactant Concentration', [InputRequired()], id='r0', description="Initial reactant concentration")
    p0 = FloatField('Starting Product Concentration', [InputRequired()], id='p0', description="Initial product concentration")
    p_end = FloatField('Final Product Concentration', [InputRequired()], id='p_end', description="Final Product concentration")
    cat_sol_conc = FloatField('Catalyst Concentration', [InputRequired()], id='cat_sol_conc',
                              description='Concentration of the catalyst solution being added to the reaction')
    inject_rate = FloatField('Injection Rate', [InputRequired()], id='inject_rate',
                             description='Rate of addition of catalyst solution to the reaction mixture')
    react_vol_init = FloatField('Initial Reactant Volume', [InputRequired()], id='react_vol_init',
                                description='Initial volume of reactant solution to which catalyst is added')
    win = IntegerField('Smoothing Window', id='win', default=1, description="Number of points in smoothing window")
    inc = IntegerField('Interpolation Multiplier', id='inc',
                       description='Number of points to interpolate between measurements', default=1)

    k_est_val = FloatField('Est Rate Constant', [InputRequired()], id='k_est_val', description="Estimated rate constant")
    k_est_min = FloatField('Min Rate Constant', [optional()], id='k_est_min',
                           description="Minimum rate constant search constraint")
    k_est_max = FloatField('Max Rate Constant', [optional()], id='k_est_max',
                           description="Maximum rate constant search constraint")

    r_ord_val = FloatField('Est Reactant Order', [InputRequired()], id='r_ord_val', default=1, description="Estimated reactant order")
    r_ord_min = FloatField('Min Reactant Order', [optional()], id='r_ord_min', default=0,
                           description="Minimum reactant order search constraint")
    r_ord_max = FloatField('Max Reactant Order', [optional()], id='r_ord_max', default=3,
                           description="Maximum reactant order search constraint")

    cat_ord_val = FloatField('Est Catalyst Order', [InputRequired()], id='c_ord_val', default=1, description="Estimated catalyst order")
    cat_ord_min = FloatField('Min Catalyst Order', [optional()], id='c_ord_min', default=0,
                             description="Minimum catalyst order search constraint")
    cat_ord_max = FloatField('Max Catalyst Order', [optional()], id='c_ord_max', default=3,
                             description="Maximum catalyst order search constraint")

    t0_est_val = FloatField('Est Start Time', [InputRequired()], id='t0_est_val', description="Estimated reaction start time")
    t0_est_min = FloatField('Min Start Time', [optional()], id='t0_est_min',
                            description="Minimum start time search constraint")
    t0_est_max = FloatField('Max Start Time', [optional()], id='t0_est_max',
                            description="Maximum start time search constraint")

    max_order = IntegerField("Maximum Order", id='max_order', default=3,
                             description="Maximum order search constraint (overrides other specific maximum constraints")

    submit = SubmitField('Fit', id='fit-submit')

    def format_k_est(self):
        if self.k_est_min.data is None or self.k_est_max.data is None:
            k_est = [self.k_est_val.data]
        else:
            k_est = [self.k_est_val.data, self.k_est_min.data, self.k_est_max.data]
        return k_est

    def format_r_ord(self):
        if self.r_ord_min.data is None or self.r_ord_max.data is None:
            r_ord = [self.r_ord_val.data]
        else:
            r_ord = [self.r_ord_val.data, self.r_ord_min.data, self.r_ord_max.data]
        return r_ord

    def format_cat_ord(self):
        if self.cat_ord_min.data is None or self.cat_ord_max.data is None:
            cat_ord = [self.cat_ord_val.data]
        else:
            cat_ord = [self.cat_ord_val.data, self.cat_ord_min.data, self.cat_ord_max.data]
        return cat_ord

    def format_t0_est(self):
        if self.t0_est_min.data is None or self.t0_est_max.data is None:
            t0_est = [self.t0_est_val.data]
        else:
            t0_est = [self.t0_est_val.data, self.t0_est_min.data, self.t0_est_max.data]
        return t0_est


class CakeDownloadForm(CakeForm):

    # File Format Tab
    f_format = StringField('f_format', default='.svg')
    image_index = IntegerField('image_index', default=0)