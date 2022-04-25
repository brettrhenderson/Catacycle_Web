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
    sheet_name = StringField('Sheet Name', id='sheet_name', description="Name of sheet in Excel file, case sensitive")
    t_col = IntegerField('Time Column', id='t_col', description="Integer index, 0 is the first column")
    tic_col = IntegerField('Total Ion Count Column', [optional()], id='tic_col', description="Integer index, 0 is the first column")
    r_col = IntegerField('Reactant Column', [optional()], id='r_col', description="Integer index, 0 is the first column")
    p_col = IntegerField('Product Column', [optional()], id='p_col', description="Integer index, 0 is the first column")
    fit_asp = SelectField('Fit Aspect', description="What trace to fit", id='fit_asp',
                            choices=[('r', 'Reactant'), ('p', 'Product'), ('rp', 'Reactant + Product')])
    scale_avg_num = IntegerField('Average Points', description="Number of points to average for calculating r0 and p_end",
                                 id='scale_avg_num', default=5)
    stoich_r = IntegerField('Reactant Coefficient', id='stoich_r', description="Stoichiometric coefficient of reactant",
                            default=1)
    stoich_p = IntegerField('Product Coefficient', id='stoich_p', description="Stoichiometric coefficient of product",
                            default=1)
    r0 = FloatField('Starting Reactant Concentration', id='r0')
    p0 = FloatField('Starting Product Concentration', id='p0')
    p_end = FloatField('Final Product Concentration', id='p_end')
    cat_add_rate = FloatField('Catalyst Addition Rate', id='cat_add_rate', description='M time_unit^-1')
    win = IntegerField('Smoothing Window', id='win', default=1)
    inc = IntegerField('Interpolation Multiplier', id='inc',
                       description='Number of points to interpolate between measurements', default=1)

    k_est_val = FloatField('Est Rate Constant', id='k_est_val')
    k_est_min = FloatField('Min Rate Constant', [optional()], id='k_est_min')
    k_est_max = FloatField('Max Rate Constant', [optional()], id='k_est_max')

    r_ord_val = FloatField('Est Reactant Order', id='r_ord_val', default=1)
    r_ord_min = FloatField('Min Reactant Order', [optional()], id='r_ord_min', default=0)
    r_ord_max = FloatField('Max Reactant Order', [optional()], id='r_ord_max', default=3)

    cat_ord_val = FloatField('Est Catalyst Order', id='c_ord_val', default=1)
    cat_ord_min = FloatField('Min Catalyst Order', [optional()], id='c_ord_min', default=0)
    cat_ord_max = FloatField('Max Catalyst Order', [optional()], id='c_ord_max', default=3)

    t0_est_val = FloatField('Est Start Time', id='t0_est_val')
    t0_est_min = FloatField('Min Start Time', [optional()], id='t0_est_min')
    t0_est_max = FloatField('Max Start Time', [optional()], id='t0_est_max')

    max_order = IntegerField("Maximum Order", id='max_order', default=3)

    submit = SubmitField('Fit')

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