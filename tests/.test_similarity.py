#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import chimera
import gaudi.parse
from pgaudi import similarity, treatment
from conftest import datapath

# Definitions
cfg = gaudi.parse.Settings(datapath("input.yaml"))
population = treatment.parse_zip(datapath("example_output/input2"))


def test_rmsd_equal():
    assert similarity.rmsd(
        population[0], population[0], *cfg.similarity.args, **cfg.similarity.kwargs
    )


def test_rmsd_dif():
    assert not similarity.rmsd(
        population[0], population[1], *cfg.similarity.args, **cfg.similarity.kwargs
    )


def test_rmsd_squared():
    coord1 = chimera.openModels.open(population[0]["Metal"])[
        0
    ].activeCoordSet.xyzArray()
    coord2 = chimera.openModels.open(population[1]["Metal"])[
        0
    ].activeCoordSet.xyzArray()
    rmsd = similarity._rmsd_squared(coord1, coord2)
    assert isinstance(rmsd, float)
    assert rmsd > 0
