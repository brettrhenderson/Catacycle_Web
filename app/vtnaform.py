from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, SelectMultipleField, FloatField
from wtforms.validators import InputRequired, ValidationError
from flask_wtf.file import FileRequired, FileField
from flask import url_for
import re

def validate_concs(form, field):
    data = field.data.replace(' ', '')
    sheets = data.split(';')
    num_concs = -1
    for sheet in sheets:
        concs = sheet.split(',')
        if '' in concs:
            concs.remove('')
        for conc in concs:
            try:
                float(conc)
            except ValueError:
                raise ValidationError("All concentrations must be numerical!")
        if num_concs != -1 and len(concs) != num_concs:
            raise ValidationError("Must include same number of starting concentrations for each reaction!")
        else:
            num_concs = len(concs)

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


class DataForm(FlaskForm):
    xl = FileField('Select Data', [FileRequired(), FlaskRegexp(r'^[a-zA-Z0-9\s_.\-\(\):]+\.xlsx$', flags=re.IGNORECASE,
                                                               message="File must have .xslx extension.")],
                   description='Upload Reaction Data in Excel file format described in "How to Format Your Data"',
                   id='excelUpload', default='/static/sampledata/Hydroamination-Kinetics-Catalyst-Order.xlsx')
    normtype = SelectField('Normalization Type', choices=[('MV', 'Max Value Normalization'),
                                                          ('TC', 'Total Count Normalization'), ('None', 'None')],
                           description='How to normalize the data.  See "Choosing data normalization method"',
                           id='normType', default='MV')

    submit = SubmitField('Plot', id="upload-submit")


class StyleForm(FlaskForm):
    units = StringField('Units', validators=[], description='Concentration Units to use for axes/legend.', id='units')
    legend = BooleanField('Legend', description="Add Legend to plot.", id='legend')
    submit = SubmitField('Apply', id='style-submit')


class SelectDataForm(FlaskForm):
    rxn = SelectMultipleField('Reaction', description='Choose which reactions to manipulate', id='rxn-select')
    species = SelectMultipleField('Species', description='Choose which Species to manipulate', id='spec-select')
    submit = SubmitField('Select', id='select-submit')


class FitParamForm(FlaskForm):
    species = StringField('Species', id="spec-param")
    excess = StringField('Excess', id='excess')
    concs = StringField('Starting Concentrations:')
    add = SubmitField('Confirm', id='add-param-submit')
    submit = SubmitField('Fit', id='param-submit')


class ManualFitForm(FlaskForm):
    start = FloatField('Align Start Time', id='start-time')
    poison = FloatField('Poisoning', id='set-poison')
    order = FloatField('Reactant Order', id='rxn-order')
    submit = SubmitField('Update', id='manual-submit')


class AutoFitForm(FlaskForm):
    start = BooleanField('Zero Data', description="Automatically fit starting time.", id='auto-zeros')
    poison = BooleanField('Assess Poisoning', description="Automatically fit the Catalyst Poisoning.", id='auto-poison')
    submit = SubmitField('Fit', id='auto-submit')


class DVTNAForm(FlaskForm):
    # File Format Tab
    f_format = SelectField('File Format', choices=[('svg', 'SVG'), ('png', 'PNG'), ('eps', 'EPS'), ('pdf', 'PDF')],
                           description='File format for downloading graph',
                           id='f_format', default='.svg')
    submit = SubmitField('Submit Download', id='download-submit')
