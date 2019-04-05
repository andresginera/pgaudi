#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pychimera import patch_environ, enable_chimera

patch_environ()
# enable_chimera()

import chimera
import random


def rmsd(ind1, ind2, threshold, subjects):
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
    diff = coords1 - coords2
    return (diff * diff).sum() / coords1.shape[0]


def remove_equal(pairs_selected, full_pop):
    for l in pairs_selected:
        for pair in l:
            if not all(i in full_pop for i in pair):
                continue
            full_pop.remove(random.choice([pair[0], pair[1]]))
