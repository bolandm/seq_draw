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
        self.sq.ax.plot([sqa['offset_x'], sqa['offset_x'] + self.duration], [sqa['offset_y'], sqa['offset_y']], **self.plot_kw)
        self.sq.ax.plot([sqa['offset_x'] + 0.1*self.duration, sqa['offset_x'] + 0.7*self.duration], [sqa['offset_y'] - self.intensity, sqa['offset_y'] + self.intensity], **self.plot_kw)
        self.sq.ax.plot([sqa['offset_x'] + 0.3 * self.duration, sqa['offset_x'] + 0.9 * self.duration],
                        [sqa['offset_y'] - self.intensity, sqa['offset_y'] + self.intensity], **self.plot_kw)


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
