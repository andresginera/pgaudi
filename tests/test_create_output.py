#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import os
import filecmp
import chimera
import gaudi.parse
from pgaudi import create_output, parallel, treatment
from conftest import datapath

# Definitions
cfg = gaudi.parse.Settings(datapath("input.yaml"))
infiles = map(
    datapath,
    [
        "example_output/input_0.yaml",
        "example_output/input_1.yaml",
        "example_output/input_2.yaml",
        "example_output/input_3.yaml",
    ],
)
pcfgs = [gaudi.parse.Settings(infile) for infile in infiles]
subpop = [treatment.parse_zip(pcfg.output.path) for pcfg in pcfgs]
population = subpop[0] + subpop[1] + subpop[2] + subpop[3]


def test_merge_log():
    create_output.merge_log(pcfgs, cfg)
    gaudi_log = os.path.join(cfg.output.path, cfg.output.name + ".gaudi-log")
    assert os.path.isfile(gaudi_log)
    assert filecmp.cmp(gaudi_log, datapath("example_output/original.gaudi-log"))


def test_generate_out():
    create_output.generate_out(population, cfg)
    gaudi_output = os.path.join(cfg.output.path, cfg.output.name + ".gaudi-output")
    assert os.path.isfile(gaudi_output)
