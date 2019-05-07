#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for the similarity and removal of double solutions.
"""

from pychimera import patch_environ, enable_chimera

patch_environ()

import chimera
import random
import copy


def rmsd(ind1, ind2, subjects, threshold, *args, **kwargs):
    """
    Function to check if two individuals are two identical solution. 

    Parameters
    ----------
    ind1, ind2 : dict
        Dictionaries representing one individual.
    threshold : float
        Maximum RMSD value to consider two individuals as similar.
        If ``rmsd > threshold``, they are considered different.
    subjects : list
        List of molecules to measure.

    Returns
    -------
    bool
        Returns True if both individuals are equal.

    """

    enable_chimera()

    molecules_1 = [chimera.openModels.open(ind1[s])[0] for s in subjects]
    molecules_2 = [chimera.openModels.open(ind2[s])[0] for s in subjects]
    for m1, m2 in zip(molecules_1, molecules_2):
        coords1 = m1.activeCoordSet.xyzArray()
        coords2 = m2.activeCoordSet.xyzArray()
        if coords1.shape[0] != coords2.shape[0]:
            return False
        rmsd_squared = _rmsd_squared(coords1, coords2)
        if rmsd_squared > threshold * threshold:
            return False
    return True


def _rmsd_squared(coords1, coords2):
    """
    Function to compute the rmsd

    Parameters
    ----------
    coords1, coords2 : array
        Array with coordinates of a molecule.

    Returns
    -------
        The rmsd results of both coordinates.

    """

    diff = coords1 - coords2
    return (diff * diff).sum() / coords1.shape[0]


def remove_equal(pairs_selected, full_pop):
    """
    Function to remove double solutions.

    Parameters
    ----------
    pairs_selected : list
        List of pairs of identical individuals.
    full_pop : list
        List of the whole populations of all subprocesses.

    """

    copy_pop = copy.deepcopy(full_pop)

    for l in pairs_selected:
        for pair in l:
            if not all(i in copy_pop for i in pair):
                continue
            copy_pop.remove(random.choice([pair[0], pair[1]]))

    return copy_pop
