import matplotlib.pyplot as plt
import numpy as np
import copy
from enum import Enum
from atoms import *
from rf_pulses import *
from gradients import *
from overlays import *
from labels import *


class SeqDiagram(object):
    def __init__(self, ax=None):
        if ax is None:
            self.ax = plt.axes([0, 0, 1, 1], frameon=False)
        else:
            self.ax = ax
        self.sqaxes = {}
        pass

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
        if (name in self.sqaxes.keys()):
            raise Exception('Axis ' + str(name) + ' alreadiy exists.')

        self.init_axis(name)
        self.sqaxes[name]['offset_x'] = offset_x
        self.sqaxes[name]['offset_y'] = offset_y
        if not (label is None):
            self.add_atom(AxisLabel(self, name, label, label_duration, plot_kw=plot_kw, font_kw=font_kw))
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

    def draw(self):
        for axis in self.sqaxes.keys():
            for pulse in self.sqaxes[axis]['atoms']:
                pulse.draw()

    def set_axis(self, atom, new_axis):
        if isinstance(atom, (list, tuple)):
            atom = [self.set_axis(a, new_axis) for a in atom]
        else:
            if isinstance(atom, AxesAtom):
                atom = copy.copy(atom)
                atom.sqaxis = new_axis
            else:
                raise Exception('Argument atom needs to be a subclass of AxisAtom or a list of AxisAtoms, but atom is ' + type(atom))
        return atom

    def get_total_duration(self, atom):
        if isinstance(atom, (list, tuple)):
            return sum([self.get_total_duration(a) for a in atom])
        else:
            if isinstance(atom, AxesAtom):
                return atom.duration
        raise Exception('Argument atom needs to be a subclass of AxisAtom or a list of AxisAtoms, but atom is ' + type(atom))
