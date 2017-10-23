#!/usr/bin/env python
# -*- coding: utf-8 -*-
import atoms
import numpy as np


class SincPulse(atoms.ArbLabeledPulse):
    def __init__(self, seq_diagram, axis, duration, intensity, side_lobes=3, label='', label_coord=None, samples=50, plot_kw={}, font_kw={}):
        pulse = np.zeros((samples + 2,))
        pulse[1:-1] = np.sinc(np.linspace(-side_lobes, side_lobes, samples))
        super(SincPulse, self).__init__(seq_diagram, axis, duration, intensity, pulse, label=label, label_coord=label_coord)
        self._update_plot_kw(plot_kw)
        self._update_font_kw(font_kw)
        pass


class HardPulse(atoms.ArbLabeledPulse):
    def __init__(self, seq_diagram, axis, duration, intensity, side_lobes=3, label='', label_coord=None, samples=50, plot_kw={}, font_kw={}):
        pulse = np.zeros((samples + 2,))
        pulse[1:-1] = np.ones_like(np.linspace(-side_lobes, side_lobes, samples))
        super(HardPulse, self).__init__(seq_diagram, axis, duration, intensity, pulse, label=label, label_coord=label_coord)
        self._update_plot_kw(plot_kw)
        self._update_font_kw(font_kw)
        pass


class HyperbolicSecantPulse(atoms.ArbLabeledPulse):
    def __init__(self, seq_diagram, axis, duration, intensity, beta=3., label='', label_coord=None, samples=50, plot_kw={}, font_kw={}):
        pulse = np.zeros((samples + 2,))
        pulse[1:-1] = 1. / np.cosh(beta * np.linspace(-1., 1., samples))
        super(HyperbolicSecantPulse, self).__init__(seq_diagram, axis, duration, intensity, pulse, label=label, label_coord=label_coord)
        self._update_plot_kw(plot_kw)
        self._update_font_kw(font_kw)
        pass


class GaussPulse(atoms.ArbLabeledPulse):
    def __init__(self, seq_diagram, axis, duration, intensity, beta=3., label='', label_coord=None, samples=50, plot_kw={}, font_kw={}):
        pulse = np.zeros((samples + 2,))
        pulse[1:-1] = np.exp(-np.square(beta) * np.square(np.linspace(-1., 1., samples)) / 2.0)
        super(GaussPulse, self).__init__(seq_diagram, axis, duration, intensity, pulse, label=label, label_coord=label_coord)
        self._update_plot_kw(plot_kw)
        self._update_font_kw(font_kw)
        pass


class HanningPulse(atoms.ArbLabeledPulse):
    """
    Hanning pulse
    Definition from :
    Dai W, Garcia D, De Bazelaire C, Alsop DC. Continuous flow-driven inversion for arterial spin labeling using pulsed
    radio frequency and gradient fields. Magn. Reson. Med. [Internet] 2008;60:1488–1497. doi: 10.1002/mrm.21790.
    """
    def __init__(self, seq_diagram, axis, duration, intensity, beta=3., label='', label_coord=None, samples=50, plot_kw={}, font_kw={}):
        pulse = np.zeros((samples + 2,))
        pulse[1:-1] = 0.5 + 0.5 * np.cos(np.linspace(-1./2., 1./2., samples) * 2.0 * np.pi)
        super(HanningPulse, self).__init__(seq_diagram, axis, duration, intensity, pulse, label=label, label_coord=label_coord)
        self._update_plot_kw(plot_kw)
        self._update_font_kw(font_kw)
        pass