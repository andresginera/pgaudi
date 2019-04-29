#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
from pgaudi import main
from conftest import datapath


def test_run():
    main.run(datapath("input.yaml"), 4, False)
