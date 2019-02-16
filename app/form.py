from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField

from wtforms.validators import DataRequired

class RatesForm(FlaskForm):

    # QuickStart tab
    num_steps = IntegerField('num-steps')
    gap = IntegerField('Gap')
    thickness = IntegerField('Thickness')

    # Step Rates tab
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

    # Incoming Arrows
    incoming1 = FloatField('incoming1')
    incoming2 = FloatField('incoming2')
    incoming3 = FloatField('incoming3')
    incoming4 = FloatField('incoming4')
    incoming5 = FloatField('incoming5')
    incoming6 = FloatField('incoming6')
    incoming7 = FloatField('incoming7')
    incoming8 = FloatField('incoming8')
    incoming9 = FloatField('incoming9')
    incoming10 = FloatField('incoming10')


    # Colors Tab
    f_color1 = FloatField('f_color1', validators=[DataRequired()])
    f_color2 = FloatField('f_color2')
    f_color3 = FloatField('f_color3')
    f_color4 = FloatField('f_color4')
    f_color5 = FloatField('f_color5')
    f_color6 = FloatField('f_color6')
    f_color7 = FloatField('f_color7')
    f_color8 = FloatField('f_color8')
    f_color9 = FloatField('f_color9')
    f_color10 = FloatField('f_color10')
    r_color1 = FloatField('r_color1')
    r_color2 = FloatField('r_color2')
    r_color3 = FloatField('r_color3')
    r_color4 = FloatField('r_color4')
    r_color5 = FloatField('r_color5')
    r_color6 = FloatField('r_color6')
    r_color7 = FloatField('r_color7')
    r_color8 = FloatField('r_color8')
    r_color9 = FloatField('r_color9')
    r_color10 = FloatField('r_color10')
    incoming_color1 = FloatField('incoming_color1')
    incoming_color2 = FloatField('incoming_color2')
    incoming_color3 = FloatField('incoming_color3')
    incoming_color4 = FloatField('incoming_color4')
    incoming_color5 = FloatField('incoming_color5')
    incoming_color6 = FloatField('incoming_color6')
    incoming_color7 = FloatField('incoming_color7')
    incoming_color8 = FloatField('incoming_color8')
    incoming_color9 = FloatField('incoming_color9')
    incoming_color10 = FloatField('incoming_color10')

    # Submit
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
