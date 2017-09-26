import atoms
import numpy as np
from enum import Enum


class GradTableType(Enum):
    ASCENDING = 1
    DESCENDING = 2
    CENTER_IN = 3
    CENTER_OUT = 4


class TrapGrad(atoms.AxesAtom):
    def __init__(self, seq_diagram, axis, duration, intensity, ft_ramp_ratio=1.0, plot_kw={}, font_kw={}):
        super(TrapGrad, self).__init__(seq_diagram)
        self.sqaxis = axis
        self.duration = duration
        self.intensity = intensity
        self._update_plot_kw(plot_kw)
        self._update_font_kw(font_kw)
        self.ft_dur = duration / (1. + 1. / ft_ramp_ratio)
        self.ramp_dur = duration / (2. * ft_ramp_ratio + 2.)

    def _draw(self):
        sqa = self.sq.sqaxes[self.sqaxis]
        # draw trapezoidal gradient
        self.sq.ax.plot([sqa['offset_x'], sqa['offset_x'] + self.ramp_dur], [sqa['offset_y'], sqa['offset_y'] + self.intensity], **self.plot_kw)
        self.sq.ax.plot([sqa['offset_x'] + self.ramp_dur, sqa['offset_x'] + self.ramp_dur + self.ft_dur], [sqa['offset_y'] + self.intensity, sqa['offset_y'] + self.intensity], **self.plot_kw)
        self.sq.ax.plot([sqa['offset_x'] + self.ramp_dur + self.ft_dur, sqa['offset_x'] + self.duration], [sqa['offset_y'] + self.intensity, sqa['offset_y']], **self.plot_kw)


class RectGrad(TrapGrad):
    def __init__(self, seq_diagram, axis, duration, intensity, plot_kw={}, font_kw={}):
        super(RectGrad, self).__init__(seq_diagram, axis, duration, intensity, ft_ramp_ratio=1e6, plot_kw=plot_kw, font_kw=font_kw)


class BlipGrad(TrapGrad):
    def __init__(self, seq_diagram, axis, duration, intensity, plot_kw={}, font_kw={}):
        super(BlipGrad, self).__init__(seq_diagram, axis, duration, intensity, ft_ramp_ratio=1e-6, plot_kw=plot_kw, font_kw=font_kw)


class TrapGradTable(atoms.AtomIterator):
    def __init__(self, seq_diagram, axis, duration, intensity_max, intensity_min, tab_steps=7, tab_type=GradTableType.ASCENDING, ft_ramp_ratio=1.0, draw_arrow=True, arrow_pos='center', plot_kw={}, font_kw={}, arrow_kw={}):
        atom = TrapGrad(seq_diagram, axis, duration, intensity_max, ft_ramp_ratio=ft_ramp_ratio, plot_kw=plot_kw, font_kw=font_kw)
        it_attr = 'intensity'
        if tab_type == GradTableType.ASCENDING:
            it_list = np.linspace(intensity_min, intensity_max, tab_steps)
        elif tab_type == GradTableType.DESCENDING:
            it_list = np.linspace(intensity_max, intensity_min, tab_steps)
        else:
            print 'Unkown GradTabletype: using ASCENDING'
            it_list = np.linspace(intensity_min, intensity_max, tab_steps)
        super(TrapGradTable, self).__init__(seq_diagram, atom, it_attr, it_list)
        self.intensity_min = intensity_min
        self.intensity_max = intensity_max
        self.tab_steps = tab_steps
        self.tab_type = tab_type
        self.draw_arrow = draw_arrow
        self.arrow_xoff = 0.
        self.arrow_yoff = 0.
        self.set_arrow_postion(arrow_pos)
        self.plot_kw = plot_kw
        self.font_kw = font_kw
        self.arrow_kw = {'length_includes_head': True,
                         'head_width': 0.06,
                         'head_length': 0.03,
                         'color': 'black'}
        for key in arrow_kw.keys():
            self.arrow_kw[key] = arrow_kw[key]

    def _draw(self):
        super(TrapGradTable, self)._draw()
        if self.draw_arrow:
            sqa = self.sq.sqaxes[self.sqaxis]
            if self.tab_type == GradTableType.ASCENDING:
                self.sq.ax.arrow(sqa['offset_x'] + self.duration + self.arrow_xoff, sqa['offset_y'] + self.intensity_min,
                                 0., self.intensity_max - self.intensity_min, **self.arrow_kw)
            elif self.tab_type == GradTableType.DESCENDING:
                self.sq.ax.arrow(sqa['offset_x'] + self.duration + self.arrow_xoff, sqa['offset_y'] + self.intensity_max,
                                 0., self.intensity_min - self.intensity_max, **self.arrow_kw)
            elif self.tab_type == GradTableType.CENTER_OUT:
                self.sq.ax.arrow(sqa['offset_x'] + self.duration + self.arrow_xoff, sqa['offset_y'],
                                 0., self.intensity_max, **self.arrow_kw)
                self.sq.ax.arrow(sqa['offset_x'] + self.duration + self.arrow_xoff, sqa['offset_y'],
                                 0., self.intensity_min, **self.arrow_kw)
            elif self.tab_type == GradTableType.CENTER_IN:
                self.sq.ax.arrow(sqa['offset_x'] + self.duration + self.arrow_xoff, sqa['offset_y'] + self.intensity_max,
                                 0., -self.intensity_max, **self.arrow_kw)
                self.sq.ax.arrow(sqa['offset_x'] + self.duration + self.arrow_xoff, sqa['offset_y'] + self.intensity_min,
                                 0., -self.intensity_min, **self.arrow_kw)
            else:
                raise Exception("")

    def set_arrow_postion(self, arrow_pos):
        if arrow_pos == 'center':
            self.arrow_xoff = -0.5 * self.duration
        elif arrow_pos == 'left':
            self.arrow_xoff = -self.duration
        elif arrow_pos == 'right':
            self.arrow_xoff = 0.
        else:
            raise Exception('Unknown arrow position')
        self.arrow_yoff = 0.1
        pass
