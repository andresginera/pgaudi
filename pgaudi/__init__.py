#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PGaudi is a package for the optimization of the performance of the GaudiMM suite by external parallelization.
It consists of five modules:

- :mod:`pgaudi.main` is the main module resposible of the main run of a pgaudi job and the parsing of arguments.
- :mod:`pgaudi.parallel` has the functions for the parallelization.
- :mod:`pgaudi.treatment` store the output individuals of the subprocesses.
- :mod:`pgaudi.similarity` defines the diversity enhancers.
- :mod:`pgaudi.create_output` is the resposible of creating all output files. 
"""

__author__ = "Andres Giner Anton"
__copyright__ = "2019, InsiliChem"
__url__ = "https://github.com/andresginera/compare-equal"
__title__ = "PGaudi"
__description__ = "A package for the optimization of the performance of the GaudiMM suite by external parallelization."
