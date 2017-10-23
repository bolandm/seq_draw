#!/usr/bin/env python
# -*- coding: utf-8 -*-
import atoms


class Interruption(atoms.AxesAtom):
    def __init__(self, seq_diagram, axis, duration, intensity, plot_kw={}):
        super(Interruption, self).__init__(seq_diagram)
        self.duration = duration
        self.intensity = intensity
        self.sqaxis = axis
        self._update_plot_kw(plot_kw)
        pass

    def _draw(self):
        sqa = self.sq.sqaxes[self.sqaxis]
        self.sq.ax.plot([sqa['offset_x'], sqa['offset_x'] + 0.35*self.duration], [sqa['offset_y'], sqa['offset_y']],
                        **self.plot_kw)
        self.sq.ax.plot([sqa['offset_x'] + 0.65 * self.duration, sqa['offset_x'] + self.duration],
                        [sqa['offset_y'], sqa['offset_y']], **self.plot_kw)
        self.sq.ax.plot([sqa['offset_x'] + 0.2*self.duration, sqa['offset_x'] + 0.6*self.duration],
                        [sqa['offset_y'] - self.intensity, sqa['offset_y'] + self.intensity], **self.plot_kw)
        self.sq.ax.plot([sqa['offset_x'] + 0.4 * self.duration, sqa['offset_x'] + 0.8 * self.duration],
                        [sqa['offset_y'] - self.intensity, sqa['offset_y'] + self.intensity], **self.plot_kw)
        pass


class AxisLabel(atoms.AxesAtom):
    def __init__(self, seq_diagram, axis, label, duration, plot_kw={}, font_kw={}):
        super(AxisLabel, self).__init__(seq_diagram)
        self.sqaxis = axis
        self.label = label
        self.duration = duration
        self.font_kw['verticalalignment'] = 'center'
        self.font_kw['horizontalalignment'] = 'center'
        self.font_kw['size'] = 'x-large'
        self._update_plot_kw(plot_kw)
        self._update_font_kw(font_kw)
        pass

    def _draw(self):
        sqa = self.sq.sqaxes[self.sqaxis]
        self.sq.ax.text(sqa['offset_x'] + self.duration / 2, sqa['offset_y'], self.label, **self.font_kw)
        pass


class Line(atoms.AxesAtom):
    def __init__(self, seq_diagram, axis, duration, plot_kw={}, font_kw={}):
        super(Line, self).__init__(seq_diagram)
        self.sqaxis = axis
        self.duration = duration
        self._update_plot_kw(plot_kw)
        self._update_font_kw(font_kw)

    def _draw(self):
        sqa = self.sq.sqaxes[self.sqaxis]
        self.sq.ax.plot([sqa['offset_x'], sqa['offset_x'] + self.duration], [sqa['offset_y'], sqa['offset_y']], **self.plot_kw)
