class Span(object):
    def __init__(self, seq_diagram, xstart, xspan, yoff, label=None, arrow_kw={}):
        self.sq = seq_diagram
        self.xstart = xstart
        self.xstop = xstart + xspan
        self.xspan = xspan
        self.xcenter = xstart + xspan / 2
        self.yoff = yoff
        self.label = label
        self.font_kw = {}
        self.font_kw['bbox'] = dict(facecolor='white', alpha=1.0, edgecolor='white')
        self.font_kw['verticalalignment'] = 'center'
        self.font_kw['horizontalalignment'] = 'center'
        self.font_kw['size'] = 'large'
        self.arrow_kw = {'length_includes_head': True,
                         'head_width': 0.05,
                         'head_length': 0.075,
                         'color': 'black'}
#         self._update_arrow_kw(arrow_kw)
        pass

    def _update_arrow_kw(self, new_kw):
        for key in new_kw.keys():
            self.arrow_kw[key] = new_kw[key]
        pass

    def _draw(self):
        self.sq.ax.arrow(self.xstart, self.yoff, self. xstop - self.xstart, 0, label=self.label, **self.arrow_kw)
        self.sq.ax.arrow(self.xstop, self.yoff, self.xstart - self.xstop, 0, label=self.label, **self.arrow_kw)
        self.sq.ax.text(self.xcenter, self.yoff, self.label, **self.font_kw)
