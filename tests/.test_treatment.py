#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
from pgaudi import treatment
from conftest import datapath


def test_parse_zip():
    population = treatment.parse_zip(datapath("example_output/input0"))
    assert isinstance(population, list)
    assert len(population) != 0
