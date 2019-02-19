from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, BooleanField

from wtforms.validators import DataRequired


class RatesForm(FlaskForm):

    MAX_ROWS = 10

    # QuickStart tab
    gap = IntegerField('gap', default=15)
    thickness = IntegerField('thickness', default=15)

    # Step Rates tab
    f_rate1 = FloatField('f_rate1', validators=[DataRequired()], default=1.0)
    f_rate2 = FloatField('f_rate2', default=0.0)
    f_rate3 = FloatField('f_rate3', default=0.0)
    f_rate4 = FloatField('f_rate4', default=0.0)
    f_rate5 = FloatField('f_rate5', default=0.0)
    f_rate6 = FloatField('f_rate6', default=0.0)
    f_rate7 = FloatField('f_rate7', default=0.0)
    f_rate8 = FloatField('f_rate8', default=0.0)
    f_rate9 = FloatField('f_rate9', default=0.0)
    f_rate10 = FloatField('f_rate10', default=0.0)
    r_rate1 = FloatField('r_rate1', default=0.0)
    r_rate2 = FloatField('r_rate2', default=0.0)
    r_rate3 = FloatField('r_rate3', default=0.0)
    r_rate4 = FloatField('r_rate4', default=0.0)
    r_rate5 = FloatField('r_rate5', default=0.0)
    r_rate6 = FloatField('r_rate6', default=0.0)
    r_rate7 = FloatField('r_rate7', default=0.0)
    r_rate8 = FloatField('r_rate8', default=0.0)
    r_rate9 = FloatField('r_rate9', default=0.0)
    r_rate10 = FloatField('r_rate10', default=0.0)

    # rate scaling
    scale_type = StringField('scale_type', default="Linear")

    # Incoming Arrows
    is_incoming1 = BooleanField('is_incoming1', default=False)
    is_incoming2 = BooleanField('is_incoming2', default=False)
    is_incoming3 = BooleanField('is_incoming3', default=False)
    is_incoming4 = BooleanField('is_incoming4', default=False)
    is_incoming5 = BooleanField('is_incoming5', default=False)
    is_incoming6 = BooleanField('is_incoming6', default=False)
    is_incoming7 = BooleanField('is_incoming7', default=False)
    is_incoming8 = BooleanField('is_incoming8', default=False)
    is_incoming9 = BooleanField('is_incoming9', default=False)
    is_incoming10 = BooleanField('is_incoming10', default=False)


    # Colors Tab
    f_color1 = StringField('f_color1', default='#4286f4')
    f_color2 = StringField('f_color2', default='#e2893b')
    f_color3 = StringField('f_color3', default='#de5eed')
    f_color4 = StringField('f_color4', default='#dd547d')
    f_color5 = StringField('f_color5', default='#4ee5ce')
    f_color6 = StringField('f_color6', default='#000000')
    f_color7 = StringField('f_color7', default='#000000')
    f_color8 = StringField('f_color8', default='#000000')
    f_color9 = StringField('f_color9', default='#000000')
    f_color10 = StringField('f_color10', default='#000000')
    r_color1 = StringField('r_color1', default='#82abed')
    r_color2 = StringField('r_color2', default='#efb683')
    r_color3 = StringField('r_color3', default='#edb2f4')
    r_color4 = StringField('r_color4', default='#ef92ae')
    r_color5 = StringField('r_color5', default='#91f2e3')
    r_color6 = StringField('r_color6', default='#000000')
    r_color7 = StringField('r_color7', default='#000000')
    r_color8 = StringField('r_color8', default='#000000')
    r_color9 = StringField('r_color9', default='#000000')
    r_color10 = StringField('r_color10', default='#000000')
    incoming_color1 = StringField('incoming_color1', default='#000000')
    incoming_color2 = StringField('incoming_color2', default='#000000')
    incoming_color3 = StringField('incoming_color3', default='#000000')
    incoming_color4 = StringField('incoming_color4', default='#000000')
    incoming_color5 = StringField('incoming_color5', default='#000000')
    incoming_color6 = StringField('incoming_color6', default='#000000')
    incoming_color7 = StringField('incoming_color7', default='#000000')
    incoming_color8 = StringField('incoming_color8', default='#000000')
    incoming_color9 = StringField('incoming_color9', default='#000000')
    incoming_color10 = StringField('incoming_color10', default='#000000')

    # Submit
    submit = SubmitField('Graph')

    def num_rows(self):
        for i in range(1, self.MAX_ROWS):
            frate = getattr(self, 'f_rate{}'.format(i)).data
            if frate and frate > 0.0:
                rows = i
            else:
                break
        return rows

    def valid(self):
        if self.f_rate1.data > 0.0:
            return True
        else:
            return False

    def draw_data(self):
        data = {'forward_rates': [],
                'rev_rates': [],
                'is_incoming': [],
                'fcolours': [],
                'rcolours': [],
                'incolours': [],
                'gap': self.gap.data,
                'thickness': self.thickness.data,
                'scale_type': self.scale_type.data}

        for i in range(1, self.MAX_ROWS+1):
            data['forward_rates'].append(getattr(self, 'f_rate{}'.format(i)).data)
            data['rev_rates'].append(getattr(self, 'r_rate{}'.format(i)).data)
            data['is_incoming'].append(getattr(self, 'is_incoming{}'.format(i)).data)
            data['fcolours'].append(getattr(self, 'f_color{}'.format(i)).data)
            data['rcolours'].append(getattr(self, 'r_color{}'.format(i)).data)
            data['incolours'].append(getattr(self, 'incoming_color{}'.format(i)).data)

        data['num_steps'] = self.num_rows()

        return data

    def default_data(self):
        data = {'forward_rates': [],
                'rev_rates': [],
                'is_incoming': [],
                'fcolours': [],
                'rcolours': [],
                'incolours': [],
                'gap': self.gap.default,
                'thickness': self.thickness.default,
                'scale_type': self.scale_type.default,
                'num_steps': 4}

        for i in range(1, self.MAX_ROWS + 1):
            data['forward_rates'].append(getattr(self, 'f_rate{}'.format(i)).default)
            data['rev_rates'].append(getattr(self, 'r_rate{}'.format(i)).default)
            data['is_incoming'].append(getattr(self, 'is_incoming{}'.format(i)).default)
            data['fcolours'].append(getattr(self, 'f_color{}'.format(i)).default)
            data['rcolours'].append(getattr(self, 'r_color{}'.format(i)).default)
            data['incolours'].append(getattr(self, 'incoming_color{}'.format(i)).default)

        # have four arrows displayed by default
        for i in range(0, 4):
            data['forward_rates'][i] = 1.0

        return data
