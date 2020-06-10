from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, BooleanField
from math import pi
from wtforms.validators import DataRequired


class RatesForm(FlaskForm):

    MAX_ROWS = 15

    # cycle selector
    plot_1 = BooleanField('plot_1', default=True)
    plot_2 = BooleanField('plot_1', default=False)
    is_vert = BooleanField('is_vert', default=False)
    p1_active = BooleanField('p1_active', default=True)

    # Styling tab
    flip = BooleanField('flip', default=False)
    rotation = IntegerField('rotation', default=0)
    translation = FloatField('translation', default=0.0)
    gap = IntegerField('gap', default=25)
    thickness = IntegerField('thickness', default=25)
    scale_type = StringField('scale_type', default="Preserve Multiples")
    swoop_width_scale = FloatField('swoop_width_scale', default=1.0)
    swoop_radius_scale = FloatField('swoop_radius_scale', default=1.0)
    swoop_sweep_scale = FloatField('swoop_sweep_scale', default=1.0)
    rel_head_width = FloatField('rel_head_width', default=2.0)
    rel_head_length_scaler = FloatField('rel_head_length_scaler', default=1.0)
    swoop_head_length_scaler = FloatField('swoop_head_length_scaler', default=1.0)
    swoop_start_angle_shift_multiplier = FloatField('swoop_start_angle_shift_multiplier', default=0.0)

    indgap = BooleanField('indgap', default=False)
    gap_1 = IntegerField('gap_1', default=25)
    gap_2 = IntegerField('gap_2', default=25)
    gap_3 = IntegerField('gap_3', default=25)
    gap_4 = IntegerField('gap_4', default=25)
    gap_5 = IntegerField('gap_5', default=25)
    gap_6 = IntegerField('gap_6', default=25)
    gap_7 = IntegerField('gap_7', default=25)
    gap_8 = IntegerField('gap_8', default=25)
    gap_9 = IntegerField('gap_9', default=25)
    gap_10 = IntegerField('gap_10', default=25)
    gap_11 = IntegerField('gap_11', default=25)
    gap_12 = IntegerField('gap_12', default=25)
    gap_13 = IntegerField('gap_13', default=25)
    gap_14 = IntegerField('gap_14', default=25)
    gap_15 = IntegerField('gap_15', default=25)

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
    f_rate11 = FloatField('f_rate11', default=0.0)
    f_rate12 = FloatField('f_rate12', default=0.0)
    f_rate13 = FloatField('f_rate13', default=0.0)
    f_rate14 = FloatField('f_rate14', default=0.0)
    f_rate15 = FloatField('f_rate15', default=0.0)
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
    r_rate11 = FloatField('r_rate11', default=0.0)
    r_rate12 = FloatField('r_rate12', default=0.0)
    r_rate13 = FloatField('r_rate13', default=0.0)
    r_rate14 = FloatField('r_rate14', default=0.0)
    r_rate15 = FloatField('r_rate15', default=0.0)


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
    is_incoming11 = BooleanField('is_incoming11', default=False)
    is_incoming12 = BooleanField('is_incoming12', default=False)
    is_incoming13 = BooleanField('is_incoming13', default=False)
    is_incoming14 = BooleanField('is_incoming14', default=False)
    is_incoming15 = BooleanField('is_incoming15', default=False)

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
    is_outgoing11 = BooleanField('is_outgoing11', default=False)
    is_outgoing12 = BooleanField('is_outgoing12', default=False)
    is_outgoing13 = BooleanField('is_outgoing13', default=False)
    is_outgoing14 = BooleanField('is_outgoing14', default=False)
    is_outgoing15 = BooleanField('is_outgoing15', default=False)


    # Colors Tab
    f_color1 = StringField('f_color1', default='#026FDD')
    f_color2 = StringField('f_color2', default='#FB7602')
    f_color3 = StringField('f_color3', default='#672CA2')
    f_color4 = StringField('f_color4', default='#BA2B2B')
    f_color5 = StringField('f_color5', default='#BC30AF')
    f_color6 = StringField('f_color6', default='#33962E')
    f_color7 = StringField('f_color7', default='#C03F17')
    f_color8 = StringField('f_color8', default='#000000')
    f_color9 = StringField('f_color9', default='#026FDD')
    f_color10 = StringField('f_color10', default='#FB7602')
    f_color11 = StringField('f_color11', default='#672CA2')
    f_color12 = StringField('f_color12', default='#BA2B2B')
    f_color13 = StringField('f_color13', default='#BC30AF')
    f_color14 = StringField('f_color14', default='#33962E')
    f_color15 = StringField('f_color15', default='#C03F17')
    r_color1 = StringField('r_color1', default='#000000')
    r_color2 = StringField('r_color2', default='#000000')
    r_color3 = StringField('r_color3', default='#000000')
    r_color4 = StringField('r_color4', default='#000000')
    r_color5 = StringField('r_color5', default='#000000')
    r_color6 = StringField('r_color6', default='#000000')
    r_color7 = StringField('r_color7', default='#000000')
    r_color8 = StringField('r_color8', default='#000000')
    r_color9 = StringField('r_color9', default='#000000')
    r_color10 = StringField('r_color10', default='#000000')
    r_color11 = StringField('r_color11', default='#000000')
    r_color12 = StringField('r_color12', default='#000000')
    r_color13 = StringField('r_color13', default='#000000')
    r_color14 = StringField('r_color14', default='#000000')
    r_color15 = StringField('r_color15', default='#000000')

    # Outside Reactions (straight arrows) tab
    f_rate_straight = FloatField('f_rate_straight', validators=[DataRequired()], default=3.0)
    r_rate_straight = FloatField('r_rate_straight', default=0.0)
    incoming_straight = BooleanField('incoming_straight', default=False)
    outgoing_straight = BooleanField('outgoing_straight', default=False)
    f_color_straight = StringField('f_color_straight', default='#000000')
    r_color_straight = StringField('r_color_straight', default='#404040')

    ###################################################################################################################
    # CYCLE 2: THIS IS A TEMPORARY AND VERY UGLY FIX
    ###################################################################################################################
    # Styling tab
    c2_flip = BooleanField('c2_flip', default=False)
    c2_rotation = IntegerField('c2_rotation', default=0)
    c2_translation = FloatField('c2_translation', default=0.0)
    c2_gap = IntegerField('c2_gap', default=25)
    c2_thickness = IntegerField('c2_thickness', default=25)
    c2_scale_type = StringField('c2_scale_type', default="Preserve Multiples")
    c2_swoop_width_scale = FloatField('c2_swoop_width_scale', default=1.0)
    c2_swoop_radius_scale = FloatField('c2_swoop_radius_scale', default=1.0)
    c2_swoop_sweep_scale = FloatField('c2_swoop_sweep_scale', default=1.0)
    c2_rel_head_width = FloatField('c2_rel_head_width', default=2.0)
    c2_rel_head_length_scaler = FloatField('c2_rel_head_length_scaler', default=1.0)
    c2_swoop_head_length_scaler = FloatField('c2_swoop_head_length_scaler', default=1.0)
    c2_swoop_start_angle_shift_multiplier = FloatField('c2_swoop_start_angle_shift_multiplier', default=0.0)

    c2_indgap = BooleanField('c2_indgap', default=False)
    c2_gap_1 = IntegerField('c2_gap_1', default=25)
    c2_gap_2 = IntegerField('c2_gap_2', default=25)
    c2_gap_3 = IntegerField('c2_gap_3', default=25)
    c2_gap_4 = IntegerField('c2_gap_4', default=25)
    c2_gap_5 = IntegerField('c2_gap_5', default=25)
    c2_gap_6 = IntegerField('c2_gap_6', default=25)
    c2_gap_7 = IntegerField('c2_gap_7', default=25)
    c2_gap_8 = IntegerField('c2_gap_8', default=25)
    c2_gap_9 = IntegerField('c2_gap_9', default=25)
    c2_gap_10 = IntegerField('c2_gap_10', default=25)
    c2_gap_11 = IntegerField('c2_gap_11', default=25)
    c2_gap_12 = IntegerField('c2_gap_12', default=25)
    c2_gap_13 = IntegerField('c2_gap_13', default=25)
    c2_gap_14 = IntegerField('c2_gap_14', default=25)
    c2_gap_15 = IntegerField('c2_gap_15', default=25)

    # Step Rates tab
    c2_f_rate1 = FloatField('c2_f_rate1', validators=[DataRequired()], default=3.0)
    c2_f_rate2 = FloatField('c2_f_rate2', default=0.0)
    c2_f_rate3 = FloatField('c2_f_rate3', default=0.0)
    c2_f_rate4 = FloatField('c2_f_rate4', default=0.0)
    c2_f_rate5 = FloatField('c2_f_rate5', default=0.0)
    c2_f_rate6 = FloatField('c2_f_rate6', default=0.0)
    c2_f_rate7 = FloatField('c2_f_rate7', default=0.0)
    c2_f_rate8 = FloatField('c2_f_rate8', default=0.0)
    c2_f_rate9 = FloatField('c2_f_rate9', default=0.0)
    c2_f_rate10 = FloatField('c2_f_rate10', default=0.0)
    c2_f_rate11 = FloatField('c2_f_rate11', default=0.0)
    c2_f_rate12 = FloatField('c2_f_rate12', default=0.0)
    c2_f_rate13 = FloatField('c2_f_rate13', default=0.0)
    c2_f_rate14 = FloatField('c2_f_rate14', default=0.0)
    c2_f_rate15 = FloatField('c2_f_rate15', default=0.0)
    c2_r_rate1 = FloatField('c2_r_rate1', default=0.0)
    c2_r_rate2 = FloatField('c2_r_rate2', default=0.0)
    c2_r_rate3 = FloatField('c2_r_rate3', default=0.0)
    c2_r_rate4 = FloatField('c2_r_rate4', default=0.0)
    c2_r_rate5 = FloatField('c2_r_rate5', default=0.0)
    c2_r_rate6 = FloatField('c2_r_rate6', default=0.0)
    c2_r_rate7 = FloatField('c2_r_rate7', default=0.0)
    c2_r_rate8 = FloatField('c2_r_rate8', default=0.0)
    c2_r_rate9 = FloatField('c2_r_rate9', default=0.0)
    c2_r_rate10 = FloatField('c2_r_rate10', default=0.0)
    c2_r_rate11 = FloatField('c2_r_rate11', default=0.0)
    c2_r_rate12 = FloatField('c2_r_rate12', default=0.0)
    c2_r_rate13 = FloatField('c2_r_rate13', default=0.0)
    c2_r_rate14 = FloatField('c2_r_rate14', default=0.0)
    c2_r_rate15 = FloatField('c2_r_rate15', default=0.0)

    # Incoming Swoops
    c2_is_incoming1 = BooleanField('c2_is_incoming1', default=False)
    c2_is_incoming2 = BooleanField('c2_is_incoming2', default=False)
    c2_is_incoming3 = BooleanField('c2_is_incoming3', default=False)
    c2_is_incoming4 = BooleanField('c2_is_incoming4', default=False)
    c2_is_incoming5 = BooleanField('c2_is_incoming5', default=False)
    c2_is_incoming6 = BooleanField('c2_is_incoming6', default=False)
    c2_is_incoming7 = BooleanField('c2_is_incoming7', default=False)
    c2_is_incoming8 = BooleanField('c2_is_incoming8', default=False)
    c2_is_incoming9 = BooleanField('c2_is_incoming9', default=False)
    c2_is_incoming10 = BooleanField('c2_is_incoming10', default=False)
    c2_is_incoming11 = BooleanField('c2_is_incoming11', default=False)
    c2_is_incoming12 = BooleanField('c2_is_incoming12', default=False)
    c2_is_incoming13 = BooleanField('c2_is_incoming13', default=False)
    c2_is_incoming14 = BooleanField('c2_is_incoming14', default=False)
    c2_is_incoming15 = BooleanField('c2_is_incoming15', default=False)

    # Outgoing Swoops
    c2_is_outgoing1 = BooleanField('c2_is_outgoing1', default=False)
    c2_is_outgoing2 = BooleanField('c2_is_outgoing2', default=False)
    c2_is_outgoing3 = BooleanField('c2_is_outgoing3', default=False)
    c2_is_outgoing4 = BooleanField('c2_is_outgoing4', default=False)
    c2_is_outgoing5 = BooleanField('c2_is_outgoing5', default=False)
    c2_is_outgoing6 = BooleanField('c2_is_outgoing6', default=False)
    c2_is_outgoing7 = BooleanField('c2_is_outgoing7', default=False)
    c2_is_outgoing8 = BooleanField('c2_is_outgoing8', default=False)
    c2_is_outgoing9 = BooleanField('c2_is_outgoing9', default=False)
    c2_is_outgoing10 = BooleanField('c2_is_outgoing10', default=False)
    c2_is_outgoing11 = BooleanField('c2_is_outgoing11', default=False)
    c2_is_outgoing12 = BooleanField('c2_is_outgoing12', default=False)
    c2_is_outgoing13 = BooleanField('c2_is_outgoing13', default=False)
    c2_is_outgoing14 = BooleanField('c2_is_outgoing14', default=False)
    c2_is_outgoing15 = BooleanField('c2_is_outgoing15', default=False)

    # Colors Tab
    c2_f_color1 = StringField('c2_f_color1', default='#026FDD')
    c2_f_color2 = StringField('c2_f_color2', default='#FB7602')
    c2_f_color3 = StringField('c2_f_color3', default='#672CA2')
    c2_f_color4 = StringField('c2_f_color4', default='#BA2B2B')
    c2_f_color5 = StringField('c2_f_color5', default='#BC30AF')
    c2_f_color6 = StringField('c2_f_color6', default='#33962E')
    c2_f_color7 = StringField('c2_f_color7', default='#C03F17')
    c2_f_color8 = StringField('c2_f_color8', default='#000000')
    c2_f_color9 = StringField('c2_f_color9', default='#026FDD')
    c2_f_color10 = StringField('c2_f_color10', default='#FB7602')
    c2_f_color11 = StringField('c2_f_color11', default='#672CA2')
    c2_f_color12 = StringField('c2_f_color12', default='#BA2B2B')
    c2_f_color13 = StringField('c2_f_color13', default='#BC30AF')
    c2_f_color14 = StringField('c2_f_color14', default='#33962E')
    c2_f_color15 = StringField('c2_f_color15', default='#C03F17')
    c2_r_color1 = StringField('c2_r_color1', default='#000000')
    c2_r_color2 = StringField('c2_r_color2', default='#000000')
    c2_r_color3 = StringField('c2_r_color3', default='#000000')
    c2_r_color4 = StringField('c2_r_color4', default='#000000')
    c2_r_color5 = StringField('c2_r_color5', default='#000000')
    c2_r_color6 = StringField('c2_r_color6', default='#000000')
    c2_r_color7 = StringField('c2_r_color7', default='#000000')
    c2_r_color8 = StringField('c2_r_color8', default='#000000')
    c2_r_color9 = StringField('c2_r_color9', default='#000000')
    c2_r_color10 = StringField('c2_r_color10', default='#000000')
    c2_r_color11 = StringField('c2_r_color11', default='#000000')
    c2_r_color12 = StringField('c2_r_color12', default='#000000')
    c2_r_color13 = StringField('c2_r_color13', default='#000000')
    c2_r_color14 = StringField('c2_r_color14', default='#000000')
    c2_r_color15 = StringField('c2_r_color15', default='#000000')

    # Outside Reactions (straight arrows) tab
    c2_f_rate_straight = FloatField('c2_f_rate_straight', validators=[DataRequired()], default=3.0)
    c2_r_rate_straight = FloatField('c2_r_rate_straight', default=0.0)
    c2_incoming_straight = BooleanField('c2_incoming_straight', default=False)
    c2_outgoing_straight = BooleanField('c2_outgoing_straight', default=False)
    c2_f_color_straight = StringField('c2_f_color_straight', default='#000000')
    c2_r_color_straight = StringField('c2_r_color_straight', default='#404040')


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

    def num_rows_c2(self):
        for i in range(1, self.MAX_ROWS+1):
            frate = getattr(self, f'c2_f_rate{i}').data
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
        data1 = {'forward_rates': [],
                 'rev_rates': [],
                 'is_incoming': [],
                 'is_outgoing': [],
                 'fcolours': [],
                 'rcolours': [],
                 'gaps': [],
                 'f_rate_straight': self.f_rate_straight.data,
                 'r_rate_straight': self.r_rate_straight.data,
                 'incoming_straight': self.incoming_straight.data,
                 'outgoing_straight': self.outgoing_straight.data,
                 'f_color_straight': self.f_color_straight.data,
                 'r_color_straight': self.r_color_straight.data,
                 'flip': self.flip.data,
                 'indgap': self.indgap.data,
                 'rotation': self.rotation.data * pi / 180,
                 'gap': self.gap.data,
                 'thickness': self.thickness.data,
                 'multiplier': float(self.thickness.data)/25.0,
                 'scale_type': self.scale_type.data,
                 'swoop_width_scale': self.swoop_width_scale.data,
                 'swoop_radius_scale': self.swoop_radius_scale.data,
                 'swoop_sweep_scale': self.swoop_sweep_scale.data,
                 'rel_head_width': self.rel_head_width.data,
                 'rel_head_length_scaler': self.rel_head_length_scaler.data,
                 'swoop_head_length_scaler': self.swoop_head_length_scaler.data,
                 'swoop_start_angle_shift_multiplier': self.swoop_start_angle_shift_multiplier.data
                }
        ########################################################################################################
        # CYCLE 2 QUICK and DIRTY
        ########################################################################################################
        data2 = {'forward_rates': [],
                 'rev_rates': [],
                 'is_incoming': [],
                 'is_outgoing': [],
                 'fcolours': [],
                 'rcolours': [],
                 'gaps': [],
                 'f_rate_straight': self.c2_f_rate_straight.data,
                 'r_rate_straight': self.c2_r_rate_straight.data,
                 'incoming_straight': self.c2_incoming_straight.data,
                 'outgoing_straight': self.c2_outgoing_straight.data,
                 'f_color_straight': self.c2_f_color_straight.data,
                 'r_color_straight': self.c2_r_color_straight.data,
                 'flip': self.c2_flip.data,
                 'indgap': self.c2_indgap.data,
                 'rotation': self.c2_rotation.data * pi / 180,
                 'gap': self.c2_gap.data,
                 'thickness': self.c2_thickness.data,
                 'multiplier': float(self.c2_thickness.data) / 25.0,
                 'scale_type': self.c2_scale_type.data,
                 'swoop_width_scale': self.c2_swoop_width_scale.data,
                 'swoop_radius_scale': self.c2_swoop_radius_scale.data,
                 'swoop_sweep_scale': self.c2_swoop_sweep_scale.data,
                 'rel_head_width': self.c2_rel_head_width.data,
                 'rel_head_length_scaler': self.c2_rel_head_length_scaler.data,
                 'swoop_head_length_scaler': self.c2_swoop_head_length_scaler.data,
                 'swoop_start_angle_shift_multiplier': self.c2_swoop_start_angle_shift_multiplier.data
        }
        for i in range(1, self.MAX_ROWS+1):
            data1['forward_rates'].append(getattr(self, 'f_rate{}'.format(i)).data)
            data1['rev_rates'].append(getattr(self, 'r_rate{}'.format(i)).data)
            data1['is_incoming'].append(getattr(self, 'is_incoming{}'.format(i)).data)
            data1['is_outgoing'].append(getattr(self, 'is_outgoing{}'.format(i)).data)
            data1['fcolours'].append(getattr(self, 'f_color{}'.format(i)).data)
            data1['rcolours'].append(getattr(self, 'r_color{}'.format(i)).data)
            data1['gaps'].append(getattr(self, 'gap_{}'.format(i)).data)
            data2['forward_rates'].append(getattr(self, 'c2_f_rate{}'.format(i)).data)
            data2['rev_rates'].append(getattr(self, 'c2_r_rate{}'.format(i)).data)
            data2['is_incoming'].append(getattr(self, 'c2_is_incoming{}'.format(i)).data)
            data2['is_outgoing'].append(getattr(self, 'c2_is_outgoing{}'.format(i)).data)
            data2['fcolours'].append(getattr(self, 'c2_f_color{}'.format(i)).data)
            data2['rcolours'].append(getattr(self, 'c2_r_color{}'.format(i)).data)
            data2['gaps'].append(getattr(self, 'c2_gap_{}'.format(i)).data)

        data1['num_steps'] = self.num_rows()
        data2['num_steps'] = self.num_rows_c2()

        return {'plot1': self.plot_1.data, 'plot2': self.plot_2.data, 'is_vert': self.is_vert.data,
                'p1_active': self.p1_active.data, 'data1': data1, 'data2': data2,  'trans1': self.translation.data,
                'trans2': self.c2_translation.data}

    def default_data(self):
        data = {'forward_rates': [],
                'rev_rates': [],
                'is_incoming': [],
                'is_outgoing': [],
                'fcolours': [],
                'rcolours': [],
                'gaps': [],
                'f_rate_straight': self.f_rate_straight.default,
                'r_rate_straight': self.r_rate_straight.default,
                'incoming_straight': self.incoming_straight.default,
                'outgoing_straight': self.outgoing_straight.default,
                'f_color_straight': self.f_color_straight.default,
                'r_color_straight': self.r_color_straight.default,
                'flip': self.flip.default,
                'indgap': self.indgap.default,
                'gap': self.gap.default,
                'thickness': self.thickness.default,
                'multiplier': float(self.thickness.default)/25.0,
                'scale_type': self.scale_type.default,
                'swoop_width_scale': self.swoop_width_scale.default,
                'swoop_radius_scale': self.swoop_radius_scale.default,
                'swoop_sweep_scale': self.swoop_sweep_scale.default,
                'rel_head_width': self.rel_head_width.default,
                'rel_head_length_scaler': self.rel_head_length_scaler.default,
                'swoop_head_length_scaler': self.swoop_head_length_scaler.default,
                'swoop_start_angle_shift_multiplier': self.swoop_start_angle_shift_multiplier.default,
                'num_steps': 4}

        for i in range(1, self.MAX_ROWS + 1):
            data['forward_rates'].append(getattr(self, 'f_rate{}'.format(i)).default)
            data['rev_rates'].append(getattr(self, 'r_rate{}'.format(i)).default)
            data['is_incoming'].append(getattr(self, 'is_incoming{}'.format(i)).default)
            data['is_outgoing'].append(getattr(self, 'is_outgoing{}'.format(i)).default)
            data['fcolours'].append(getattr(self, 'f_color{}'.format(i)).default)
            data['rcolours'].append(getattr(self, 'r_color{}'.format(i)).default)
            data['gaps'].append(getattr(self, 'gap_{}'.format(i)).default)

        # have four arrows displayed by default
        for i in range(0, 4):
            data['forward_rates'][i] = 3.0

        return {'plot1': True, 'plot2': False, 'is_vert': False, 'p1_active': True, 'data1': data,
                'trans1': 0, 'trans2': 0}


class DownloadForm(RatesForm):

    # File Format Tab
    f_format = StringField('f_format', default='.svg')
    image_index = IntegerField('image_index', default=0)

    def draw_data(self):
        data = super().draw_data()
        data['f_format'] = self.f_format.data
        print(f'\n\nFILE FORMAT: {self.f_format.data}\n\n')
        data['image_index'] = self.image_index.data
        return data
