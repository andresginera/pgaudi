#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import gaudi.parse
import subprocess
import itertools
import os
from conftest import datapath
from pgaudi import parallel, treatment

# Definitions
yaml = datapath("input.yaml")
cfg = gaudi.parse.Settings(yaml)
population_1 = treatment.parse_zip(datapath("example_output/input2"))
population_2 = treatment.parse_zip(datapath("example_output/input3"))
pair_list = [population_1, population_2]


def test_divide_cfg():
    pcfg_names, pcfgs = parallel.divide_cfg(cfg, 4, False)
    assert isinstance(pcfg_names, list)
    assert isinstance(pcfgs, list)
    assert len(pcfg_names) != 0
    assert len(pcfgs) != 0
    for name in pcfg_names:
        assert os.path.isfile(name)
        os.remove(name)


def test_gaudi_parallel():
    e = subprocess.call("gaudi run {}".format(yaml), shell=True)
    assert e == 0


def test_similarity_parallel():
    pairs_selected = parallel.similarity_parallel(pair_list, cfg)
    assert isinstance(pairs_selected, list)
    assert len(pairs_selected) != 0

