from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField

from wtforms.validators import DataRequired

class RatesForm(FlaskForm):
    f_rate1 = FloatField('f_rate1', validators=[DataRequired()])
    f_rate2 = FloatField('f_rate2')
    f_rate3 = FloatField('f_rate3')
    f_rate4 = FloatField('f_rate4')
    f_rate5 = FloatField('f_rate5')
    f_rate6 = FloatField('f_rate6')
    f_rate7 = FloatField('f_rate7')
    f_rate8 = FloatField('f_rate8')
    f_rate9 = FloatField('f_rate9')
    f_rate10 = FloatField('f_rate10')
    r_rate1 = FloatField('r_rate1')
    r_rate2 = FloatField('r_rate2')
    r_rate3 = FloatField('r_rate3')
    r_rate4 = FloatField('r_rate4')
    r_rate5 = FloatField('r_rate5')
    r_rate6 = FloatField('r_rate6')
    r_rate7 = FloatField('r_rate7')
    r_rate8 = FloatField('r_rate8')
    r_rate9 = FloatField('r_rate9')
    r_rate10 = FloatField('r_rate10')
    submit = SubmitField('Graph')

    def num_rows(self):
        for i in range(1,11):
            frate = getattr(self, 'f_rate{}'.format(i)).data
            if frate and frate > 0.0:
                rows = i
            else:
                break
        return rows

    def values(self):
        data = {}
        for i in range(1, 11):
            frate = getattr(self, 'f_rate{}'.format(i)).data
            rrate = getattr(self, 'r_rate{}'.format(i)).data
            data['f_rate{}'.format(i)] = frate or 0.0
            data['r_rate{}'.format(i)] = rrate or 0.0
        return data

    def no_data(self):
        data = {}
        for i in range(1, 11):
            data['f_rate{}'.format(i)] = 0.0
            data['r_rate{}'.format(i)] = 0.0
        return data

    def valid(self):
        if self.f_rate1.data > 0.0:
            return True
        else:
            return False
