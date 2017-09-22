import atoms
import numpy as np


class SincPulse(atoms.ArbLabeledPulse):
    def __init__(self, seq_diagram, axis, duration, intensity, side_lobes=3, label='', label_coord=None, samples=50):
        pulse = np.zeros((samples + 2,))
        pulse[1:-1] = np.sinc(np.linspace(-side_lobes, side_lobes, samples))
        super(SincPulse, self).__init__(seq_diagram, axis, duration, intensity, pulse, label=label, label_coord=label_coord)


class HyperbolicSecantPulse(atoms.ArbLabeledPulse):
    def __init__(self, seq_diagram, axis, duration, intensity, beta=3., label='', label_coord=None, samples=50):
        pulse = np.zeros((samples + 2,))
        pulse[1:-1] = 1. / np.cosh(beta * np.linspace(-1., 1., samples))
        super(HyperbolicSecantPulse, self).__init__(seq_diagram, axis, duration, intensity, pulse, label=label, label_coord=label_coord)


class GaussPulse(atoms.ArbLabeledPulse):
    def __init__(self, seq_diagram, axis, duration, intensity, beta=3., label='', label_coord=None, samples=50):
        pulse = np.zeros((samples + 2,))
        pulse[1:-1] = np.exp(-np.square(beta) * np.square(np.linspace(-1., 1., samples)) / 2.0)
        super(GaussPulse, self).__init__(seq_diagram, axis, duration, intensity, pulse, label=label, label_coord=label_coord)
