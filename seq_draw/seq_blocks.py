import atoms
import misc
import gradients
import rf_pulses
import copy
import numpy as np


def repeat_atom(seq_diagram, axis, proto_atom, n_rep, dur, intensity, init_shift=None, total_dur=None, plot_kw={}):
    '''
    Repeats an AxesAtom
    :param seq_diagram: Sequence diagram object
    :param axis: Axis name
    :param n_rep: Number of repeats
    :param dur: Duration of readout gradient
    :param intensity: Intensity of readout gradient
    :param init_shift: Initial time shift
    :param total_dur: Total length of all objects in list
    :param proto_atom: Prototype atom
    :param plot_kw: Additional plot arguments
    :return: List of AxisAtoms
    '''
    assert (isinstance(proto_atom, atoms.AxesAtom))

    multiple_durations = False
    if isinstance(dur, (list, tuple, set)):
        if not (len(dur) == n_rep):
            raise Exception('Length of durations {0} not equal to nrep {1}'.format(len(dur), n_rep))
        multiple_durations = True

    multiple_intensities = False
    if isinstance(intensity, (list, tuple, set)):
        if not (len(intensity) == n_rep):
            raise Exception('Length of intensity {0} not equal to nrep {1}'.format(len(intensity), n_rep))
        multiple_intensities = True

    rep_atoms = list()
    if not (init_shift is None):
        rep_atoms.append(misc.Line(seq_diagram, axis, init_shift, plot_kw=plot_kw))

    _dur = dur
    _intensity = intensity
    for i in range(n_rep):
        if multiple_durations:
            _dur = dur[i]
        if multiple_intensities:
            _intensity = intensity[i]
        proto_atom.intensity = _intensity
        proto_atom.duration = _dur
        rep_atoms.append(copy.copy(proto_atom))

    if not (total_dur is None):
        epi_dur = sum([atom.duration for atom in rep_atoms])
        if total_dur > epi_dur:
            rep_atoms.append(misc.Line(seq_diagram, axis, total_dur - epi_dur, plot_kw=plot_kw))

    return rep_atoms


def repeat_atom_spaced(seq_diagram, axis, proto_atom, n_rep, dur, intensity, spacing, init_shift= None, total_dur=None, proto_space=None, plot_kw={}):
    """
    Repeats an AxesAtom
    :param seq_diagram: Sequence diagram object
    :param axis: Axis name
    :param n_rep: Number of repeats
    :param dur: Duration of readout gradient
    :param intensity: Intensity of readout gradient
    :param spacing: Spacing of individual elements
    :param init_shift: Initial time shift
    :param total_dur: Total length of all objects in list
    :param proto_atom: Prototype atom
    :param plot_kw: Additional plot arguments
    :return: List of AxisAtoms
    """
    assert(spacing >= dur)
    assert(isinstance(proto_atom, atoms.AxesAtom))

    if proto_space is None:
        proto_space = misc.Line(seq_diagram, axis, spacing - dur, plot_kw=plot_kw)

    if init_shift is None:
        init_shift = spacing - dur/2

    multiple_intensities = False
    if isinstance(intensity, (list, tuple, set)):
        if not (len(intensity) == n_rep):
            raise Exception('Length of intensity {0} not equal to nrep {1}'.format(len(intensity), n_rep))
        multiple_intensities = True

    rep_atoms = list()
    rep_atoms.append(misc.Line(seq_diagram, axis, init_shift - dur / 2.0, plot_kw=plot_kw))

    _intensity = intensity
    _spacing = spacing - dur
    for i in range(n_rep):
        if multiple_intensities:
            _intensity = intensity[i]
        proto_atom.intensity = _intensity
        proto_atom.duration = dur
        rep_atoms.append(copy.copy(proto_atom))
        proto_space.duration = _spacing
        rep_atoms.append(copy.copy(proto_space))

    if not (total_dur is None):
        epi_dur = sum([atom.duration for atom in rep_atoms])
        if total_dur > epi_dur:
            rep_atoms.append(misc.Line(seq_diagram, axis, total_dur - epi_dur, plot_kw=plot_kw))

    return rep_atoms


def get_epi_readout(seq_diagram, axis, n_rep, read_dur, read_intensity, init_shift=None, total_dur=None, read_grad=None, plot_kw={}):
    if isinstance(read_intensity, (float, int)):
        read_intensity = [read_intensity*2.*((i % 2) - 0.5) for i in range(n_rep)]
    if read_grad is None:
        read_grad = gradients.TrapGrad(seq_diagram, axis, read_dur, read_intensity, plot_kw=plot_kw)
    return repeat_atom(seq_diagram, axis, read_grad, n_rep, read_dur, read_intensity, init_shift, total_dur, plot_kw)


def get_epi_blips(seq_diagram, axis, n_rep, blip_dur, blip_intensity, blip_spacing, blip_pattern=[1.0], init_shift=None, total_dur=None, blip_grad=None, plot_kw={}):
    assert(isinstance(blip_intensity, (float, int)))

    if blip_grad is None:
        blip_grad = gradients.BlipGrad(seq_diagram, axis, blip_dur, blip_intensity, plot_kw=plot_kw)

    blip_pattern *= int(n_rep / len(blip_pattern) + 1)
    blip_intensity = [blip_intensity * blip for blip in blip_pattern[:n_rep]]

    return repeat_atom_spaced(seq_diagram, axis, blip_grad, n_rep, blip_dur, blip_intensity, blip_spacing, init_shift, total_dur=total_dur, plot_kw=plot_kw)