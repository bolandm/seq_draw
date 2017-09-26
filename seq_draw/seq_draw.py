import matplotlib.pyplot as plt
import copy
import atoms
import misc


class SeqDiagram(object):
    def __init__(self, ax=None):
        if ax is None:
            self.ax = plt.axes([0, 0, 1, 1], frameon=False)
        else:
            self.ax = ax
        self.sqaxes = {}
        pass

    def __str__(self):
        _str = ''
        for axis in self.sqaxes.keys():
            _str += 'Axis {0:s}:\n'.format(axis)
            time_sum = 0.0
            for i, atom in enumerate(self.sqaxes[axis]['atoms']):
                _str += '  {0:2.3f}: {1:s}\n'.format(time_sum, atom)
                time_sum += atom.duration
            _str += 'Sum {0:2.3f}\n'.format(time_sum)
        return _str

    __repr__ = __str__

    @property
    def ax(self):
        return self._ax

    @ax.setter
    def ax(self, new_ax):
        self._ax = new_ax
        # remove locators
        self._ax.axes.get_xaxis().set_visible(False)
        self._ax.axes.get_yaxis().set_visible(False)
        pass

    def add_axis(self, name, offset_x, offset_y, label=None, label_duration=0.9, plot_kw={}, font_kw={}):
        if name in self.sqaxes.keys():
            raise Exception('Axis ' + str(name) + ' alreadiy exists.')

        self.init_axis(name)
        self.sqaxes[name]['offset_x'] = offset_x
        self.sqaxes[name]['offset_y'] = offset_y
        self.sqaxes[name]['offset_x_init'] = offset_x
        self.sqaxes[name]['offset_y_init'] = offset_y
        if not (label is None):
            self.add_atom(misc.AxisLabel(self, name, label, label_duration, plot_kw=plot_kw, font_kw=font_kw))
        pass

    def init_axis(self, name):
        self.sqaxes[name] = {'offset_x': 0.0, 'offset_y': 0.0, 'atoms': list()}
        pass

    def reset_axis(self, name, keep_first=1):
        del self.sqaxes[name]['atoms'][keep_first:]
        pass

    def init_axes(self, label_duration=0.5, plot_kw={}, font_kw={}):
        self.add_axis('rf', 0.0, 0.7, 'RF', label_duration)
        self.add_axis('gx', 0.0, 0.5, 'GX', label_duration)
        self.add_axis('gy', 0.0, 0.3, 'GY', label_duration)
        self.add_axis('gz', 0.0, 0.1, 'GZ', label_duration)
        pass

    def reset_axes(self):
        for axis in self.sqaxes.keys():
            self.reset_axis(axis)

    def add_atom(self, atom):
        if isinstance(atom, (list, tuple)):
            for a in atom:
                self.add_atom(a)
        else:
            if atom.sqaxis in self.sqaxes.keys():
                self.sqaxes[atom.sqaxis]['atoms'].append(atom)
            else:
                raise Exception('Unknown axis ' + atom.sqaxis + '. Possible values are ' + str(self.sqaxes.keys()))

    def draw(self, debug=False, debug_intensity=0.075, debug_labels=True):
        for axis in self.sqaxes.keys():
            for i, pulse in enumerate(self.sqaxes[axis]['atoms']):
                pulse.draw()
                if debug:
                    pulse.draw_debug(intensity=debug_intensity, label=debug_labels, index=i)
        # reset origin
        for axis in self.sqaxes.keys():
            self.sqaxes[axis]['offset_x'] = self.sqaxes[axis]['offset_x_init']
            self.sqaxes[axis]['offset_y'] = self.sqaxes[axis]['offset_y_init']

    def set_axis(self, atom, new_axis):
        if isinstance(atom, (list, tuple)):
            atom = [self.set_axis(a, new_axis) for a in atom]
        else:
            if isinstance(atom, atoms.AxesAtom):
                atom = copy.copy(atom)
                atom.sqaxis = new_axis
            else:
                raise Exception('Argument atom needs to be a subclass of AxisAtom or a list of AxisAtoms, but atom is ' + type(atom))
        return atom

    def get_total_duration(self, atom):
        if isinstance(atom, (list, tuple)):
            return sum([self.get_total_duration(a) for a in atom])
        else:
            if isinstance(atom, atoms.AxesAtom):
                return atom.duration
        raise Exception('Argument atom needs to be a subclass of AxisAtom or a list of AxisAtoms, but atom is ' + type(atom))

    def fill(self, axes=None, plot_kw={}):
        if axes is None:
            axes = self.sqaxes.keys()

        # compute sum
        sums = {}
        max_sum = 0.0
        max_ax = axes[0]
        for ax in axes:
            sums[ax] = 0.0
            for atom in self.sqaxes[ax]['atoms']:
                sums[ax] += atom.duration
            if max_sum < sums[ax]:
                max_sum = sums[ax]
                max_ax = ax
        for ax in set(axes) - set(ax):
            self.add_atom(misc.Line(self, ax, max_sum - sums[ax], plot_kw=plot_kw))
        pass
