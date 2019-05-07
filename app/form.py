from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, BooleanField

from wtforms.validators import DataRequired


class RatesForm(FlaskForm):

    MAX_ROWS = 10

    # Styling tab
    gap = IntegerField('gap', default=25)
    thickness = IntegerField('thickness', default=25)
    scale_type = StringField('scale_type', default="Preserve Multiples")

    # Step Rates tab
    f_rate1 = FloatField('f_rate1', validators=[DataRequired()], default=3.0)
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


    # Incoming Swoops
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

    # Outgoing Swoops
    is_outgoing1 = BooleanField('is_outgoing1', default=False)
    is_outgoing2 = BooleanField('is_outgoing2', default=False)
    is_outgoing3 = BooleanField('is_outgoing3', default=False)
    is_outgoing4 = BooleanField('is_outgoing4', default=False)
    is_outgoing5 = BooleanField('is_outgoing5', default=False)
    is_outgoing6 = BooleanField('is_outgoing6', default=False)
    is_outgoing7 = BooleanField('is_outgoing7', default=False)
    is_outgoing8 = BooleanField('is_outgoing8', default=False)
    is_outgoing9 = BooleanField('is_outgoing9', default=False)
    is_outgoing10 = BooleanField('is_outgoing10', default=False)


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

    # Outside Reactions (straight arrows) tab
    f_rate_straight = FloatField('f_rate_straight', validators=[DataRequired()], default=3.0)
    r_rate_straight = FloatField('r_rate_straight', default=0.0)
    incoming_straight = BooleanField('incoming_straight', default=False)
    outgoing_straight = BooleanField('outgoing_straight', default=False)
    f_color_straight = StringField('f_color_straight', default='#000000')
    r_color_straight = StringField('r_color_straight', default='#333333')

    # Submit
    submit = SubmitField('Graph')

    def num_rows(self):
        for i in range(1, self.MAX_ROWS+1):
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
                'is_outgoing': [],
                'fcolours': [],
                'rcolours': [],
                'f_rate_straight': self.f_rate_straight.data,
                'r_rate_straight': self.r_rate_straight.data,
                'incoming_straight': self.incoming_straight.data,
                'outgoing_straight': self.outgoing_straight.data,
                'f_color_straight': self.f_color_straight.data,
                'r_color_straight': self.r_color_straight.data,
                'gap': self.gap.data,
                'thickness': self.thickness.data,
                'multiplier': float(self.thickness.data)/25.0,
                'scale_type': self.scale_type.data,
                }

        for i in range(1, self.MAX_ROWS+1):
            data['forward_rates'].append(getattr(self, 'f_rate{}'.format(i)).data)
            data['rev_rates'].append(getattr(self, 'r_rate{}'.format(i)).data)
            data['is_incoming'].append(getattr(self, 'is_incoming{}'.format(i)).data)
            data['is_outgoing'].append(getattr(self, 'is_outgoing{}'.format(i)).data)
            data['fcolours'].append(getattr(self, 'f_color{}'.format(i)).data)
            data['rcolours'].append(getattr(self, 'r_color{}'.format(i)).data)

        data['num_steps'] = self.num_rows()

        return data

    def default_data(self):
        data = {'forward_rates': [],
                'rev_rates': [],
                'is_incoming': [],
                'is_outgoing': [],
                'fcolours': [],
                'rcolours': [],
                'f_rate_straight': self.f_rate_straight.default,
                'r_rate_straight': self.r_rate_straight.default,
                'incoming_straight': self.incoming_straight.default,
                'outgoing_straight': self.outgoing_straight.default,
                'f_color_straight': self.f_color_straight.default,
                'r_color_straight': self.r_color_straight.default,
                'gap': self.gap.default,
                'thickness': self.thickness.default,
                'multiplier': float(self.thickness.default)/25.0,
                'scale_type': self.scale_type.default,
                'num_steps': 4}

        for i in range(1, self.MAX_ROWS + 1):
            data['forward_rates'].append(getattr(self, 'f_rate{}'.format(i)).default)
            data['rev_rates'].append(getattr(self, 'r_rate{}'.format(i)).default)
            data['is_incoming'].append(getattr(self, 'is_incoming{}'.format(i)).default)
            data['is_outgoing'].append(getattr(self, 'is_outgoing{}'.format(i)).default)
            data['fcolours'].append(getattr(self, 'f_color{}'.format(i)).default)
            data['rcolours'].append(getattr(self, 'r_color{}'.format(i)).default)

        # have four arrows displayed by default
        for i in range(0, 4):
            data['forward_rates'][i] = 3.0

        return data


class DownloadForm(RatesForm):

    # File Format Tab
    f_format = StringField('f_format', default='.svg')
    image_index = IntegerField('image_index', default=0)

    def draw_data(self):
        data = super().draw_data()
        data['f_format'] = self.f_format.data
        data['image_index'] = self.image_index.data
        return data