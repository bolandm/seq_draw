#!/usr/bin/env python
# -*- coding: utf-8 -*-
class OverlayObject(object):
    def __init__(self, seq_diagram, plot_kw={}, font_kw={}):
        self.sq = seq_diagram
        self.font_kw = {}
        self.plot_kw = {}
        pass

    def _update_plot_kw(self, new_kw):
        for key in new_kw.keys():
            self.plot_kw[key] = new_kw[key]
        pass

    def _update_font_kw(self, new_kw):
        for key in new_kw.keys():
            self.font_kw[key] = new_kw[key]
        pass

    def _draw(self):
        pass

    def draw(self):
        self._draw()
        pass


class TimeSpan(OverlayObject):
    def __init__(self, seq_diagram, xstart, xspan, yoff, label=None, plot_kw={}, font_kw={}, arrow_kw={}):
        super(TimeSpan, self).__init__(seq_diagram, plot_kw=plot_kw, font_kw=font_kw)
        self.xstart = xstart
        self.xstop = xstart + xspan
        self.xspan = xspan
        self.xcenter = xstart + xspan / 2
        self.yoff = yoff
        self.label = label
        self._update_plot_kw(plot_kw)
        self._update_font_kw(font_kw)
        self.font_kw['bbox'] = dict(facecolor='white', alpha=1.0, edgecolor='white')
        self.font_kw['verticalalignment'] = 'center'
        self.font_kw['horizontalalignment'] = 'center'
        self.font_kw['size'] = 'large'
        self.arrow_kw = {'length_includes_head': True,
                         'head_width': 0.05,
                         'head_length': 0.075,
                         'color': 'black'}
        self._update_arrow_kw(arrow_kw)
        pass

    def _update_arrow_kw(self, new_kw):
        for key in new_kw.keys():
            self.arrow_kw[key] = new_kw[key]
        pass

    def _draw(self):
        self.sq.ax.arrow(self.xstart, self.yoff, self. xstop - self.xstart, 0, label=self.label, **self.arrow_kw)
        self.sq.ax.arrow(self.xstop, self.yoff, self.xstart - self.xstop, 0, label=self.label, **self.arrow_kw)
        self.sq.ax.text(self.xcenter, self.yoff, self.label, **self.font_kw)


class VerticalLine(OverlayObject):
    def __init__(self, seq_diagram, xpos, ymin=0., ymax=0.9, plot_kw={}):
        super(VerticalLine, self).__init__(seq_diagram, plot_kw=plot_kw)
        self.xpos = xpos
        self.ymin = ymin
        self.ymax = ymax
        self.plot_kw['color'] = 'black'
        self._update_plot_kw(plot_kw)

    def _draw(self):
        self.sq.ax.plot([self.xpos, self.xpos], [self.ymin, self.ymax], **self.plot_kw)


class Bra(VerticalLine):
    def __init__(self, seq_diagram, xpos, xlen=0.3, ymin=0., ymax=0.85, plot_kw={}):
        super(Bra, self).__init__(seq_diagram, xpos, ymin=ymin, ymax=ymax, plot_kw=plot_kw)
        self.xlen = xlen

    def _draw(self):
        super(Bra, self)._draw()
        self.sq.ax.plot([self.xpos, self.xpos + self.xlen], [self.ymin, self.ymin], **self.plot_kw)
        self.sq.ax.plot([self.xpos, self.xpos + self.xlen], [self.ymax, self.ymax], **self.plot_kw)


class Ket(Bra):
    def __init__(self, seq_diagram, xpos, xlen=0.3, ymin=0., ymax=0.85, plot_kw={}):
        super(Ket, self).__init__(seq_diagram, xpos, xlen=xlen, ymin=ymin, ymax=ymax, plot_kw=plot_kw)
        self.xlen = -xlen


class VerticalSpan(OverlayObject):
    def __init__(self, seq_diagram, xmin, xmax, ymin=0., ymax=0.85, plot_kw={}):
        super(VerticalSpan, self).__init__(seq_diagram, plot_kw=plot_kw)
        self.xmax = xmax
        self.xmin = xmin
        self.ymin = ymin
        self.ymax = ymax
        self.plot_kw['alpha'] = 0.25
        self._update_plot_kw(plot_kw)

    def _draw(self):
        from matplotlib.patches import Rectangle
        self.sq.ax.add_patch(Rectangle((self.xmin, self.ymin), self.xmax - self.xmin, self.ymax - self.ymin, **self.plot_kw))
        # self.sq.ax.axes.axvspan(self.xmin, self.xmax, self.ymin, self.ymax, **self.plot_kw)


