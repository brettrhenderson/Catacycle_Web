from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import InputRequired, regexp, ValidationError
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

class VTNAForm(FlaskForm):
    #, regexp(r'^[a-zA-Z0-9\s_.\-\(\):]+\.xlsx$', flags=re.IGNORECASE)
    xl = FileField('Upload Data', [FileRequired()],
                   description='Upload Reaction Data in Excel file format described in "How to Format Your Data"',
                   id='excelUpload', default='/static/sampledata/Hydroamination-Kinetics-Catalyst-Order.xlsx')

    concs = StringField('Starting Concentrations:', [InputRequired(), validate_concs],
                        description='Input starting concentrations for each reaction as described in "How to Format '
                                    'Concentrations"',
                        id='startConcs', default='0.0510; 0.0578; 0.0688; 0.0750; 0.104; 0.125; 0.127; 0.142')

    units = StringField('Units:', validators=[], description='Concentration Units to Use', id='units', default="uM")

    auto = BooleanField('Auto Fit', description="Automatically fit the order of the reaction.", id='autoFit',
                        default=False)

    poison = BooleanField('Assess Poisoning', description="Automatically fit the Catalyst Poisoning.", id='poison',
                        default=False)

    normtype = SelectField('Normalization Type', choices=[('MV', 'Max Value Normalization'),
                                                          ('TC', 'Total Count Normalization'), ('None', 'None')],
                           description='How to normalize the data.  See "Choosing data normalization method"',
                           id='normType', default='MV')