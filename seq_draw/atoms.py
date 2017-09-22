import matplotlib.pyplot as plt
import numpy as np


class AxesAtom(object):
    def __init__(self, seq_diagram):
        self.sq = seq_diagram
        self._sqaxis = self.sq.sqaxes.keys()[0]
        self._duration = 0.0
        self._do_update_origin = True
        self._plot_kw = {'color': 'black', 'linestyle': 'solid'}
        self._font_kw = {}
        self._origin = None
        pass

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, origin):
        self._origin = origin
        pass

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @property
    def sqaxis(self):
        return self._sqaxis

    @sqaxis.setter
    def sqaxis(self, axis):
        self._sqaxis = axis
        pass

    @property
    def plot_kw(self):
        return self._plot_kw

    @plot_kw.setter
    def plot_kw(self, plot_kw):
        self._plot_kw = plot_kw
        pass

    @property
    def font_kw(self):
        return self._font_kw

    @font_kw.setter
    def font_kw(self, font_kw):
        self._font_kw = font_kw
        pass

    @property
    def do_update_origin(self):
        return self._do_update_origin

    @do_update_origin.setter
    def do_update_origin(self, do_update_origin):
        self._do_update_origin = do_update_origin
        pass

    def draw(self):
        self._draw()
        if self.do_update_origin:
            self.update_origin()
        pass

    def _update_plot_kw(self, new_kw):
        for key in new_kw.keys():
            self.plot_kw[key] = new_kw[key]
        pass

    def _update_font_kw(self, new_kw):
        for key in new_kw.keys():
            self.font_kw[key] = new_kw[key]
        pass

    def update_origin(self):
        self.origin = (self.sq.sqaxes[self.sqaxis]['offset_x'],
                       self.sq.sqaxes[self.sqaxis]['offset_y'])
        self.sq.sqaxes[self.sqaxis]['offset_x'] += self.duration
        pass


class ArbitraryPulse(AxesAtom):
    def __init__(self, seq_diagram, axis, duration, intensity, pulse):
        super(ArbitraryPulse, self).__init__(seq_diagram)
        self.sqaxis = axis
        self.duration = duration
        self.intensity = intensity
        self.pulse = pulse
        pass

    def _draw(self):
        sqa = self.sq.sqaxes[self.sqaxis]
        self.sq.ax.plot(np.linspace(sqa['offset_x'], sqa['offset_x'] + self.duration, len(self.pulse)), self.pulse * self.intensity + sqa['offset_y'], **self.plot_kw)
        pass


class ArbLabeledPulse(ArbitraryPulse):
    def __init__(self, seq_diagram, axis, duration, intensity, pulse, label='', label_coord=None):
        super(ArbLabeledPulse, self).__init__(seq_diagram, axis, duration, intensity, pulse)
        if label_coord is None:
            self.label_coord = (0, self.intensity)
        else:
            if not (isinstance(label_coord, (list, tuple, set)) and (len(label_coord) == 2)):
                raise Exception('Provided label coordinates ' + str(label_coord) + ' not supported.')
            self.label_coord = label_coord
        self.label = label
        self.font_kw['verticalalignment'] = 'top'
        self.font_kw['horizontalalignment'] = 'left'
        self.font_kw['size'] = 'medium'
        pass

    def _draw(self):
        # draw pulse
        super(ArbLabeledPulse, self)._draw()
        # draw label
        sqa = self.sq.sqaxes[self.sqaxis]
        self.sq.ax.text(sqa['offset_x'] + self.label_coord[0], sqa['offset_y'] + self.label_coord[1], self.label, **self.font_kw)
        pass


class AtomIterator(AxesAtom):
    def __init__(self, seq_diagram, atom, it_attr, it_list):
        super(AtomIterator, self).__init__(seq_diagram)
        self.sq = seq_diagram
        self.atom = atom
        self.it_attr = it_attr
        self.it_list = it_list
        if isinstance(it_attr, (list, tuple, set)):
            for _it_attr in it_attr:
                if not hasattr(self.atom, _it_attr):
                    raise Exception('Provided atom ({0}) has no attribute {1}'.format(self.atom, _it_attr))
            if not isinstance(it_list, (list, tuple, set)):
                raise Exception('it_list is not one of (list, tuple, set)')
            if not (len(it_attr) == len(it_list)):
                raise Exception('Length of it_attr and it_list must be equal')
        else:
            if not hasattr(self.atom, self.it_attr):
                raise Exception('Provided atom ({0}) has no attribute {1}'.format(self.atom, self.it_attr))
            self.it_attr = [it_attr]
            self.it_list = [it_list]

    @property
    def origin(self):
        return self.atom.origin

    @origin.setter
    def origin(self, origin):
        self.atom.origin = origin
        pass

    @property
    def duration(self):
        return self.atom.duration

    @duration.setter
    def duration(self, duration):
        self.atom.duration = duration
        pass

    @property
    def sqaxis(self):
        return self.atom.sqaxis

    @sqaxis.setter
    def sqaxis(self, axis):
        self.atom.sqaxis = axis
        pass

    @property
    def plot_kw(self):
        return self.atom.plot_kw

    @plot_kw.setter
    def plot_kw(self):
        self.atom.plot_kw = plot_kw
        pass

    @property
    def font_kw(self):
        return self.atom.font_kw

    @font_kw.setter
    def font_kw(self, font_kw):
        self.atom.font_kw = font_kw
        pass

    @property
    def do_update_origin(self):
        return self.atom.do_update_origin

    @do_update_origin.setter
    def do_update_origin(self, do_update_origin):
        self.atom.do_update_origin = do_update_origin
        pass

    def _draw(self):
        for i in range(len(self.it_list[0])):
            for _attr, _val in zip(self.it_attr, self.it_list):
                setattr(self.atom, _attr, _val[i])
            self.atom._draw()
