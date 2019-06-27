#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############
#   PGaudi: A package for optimize the performance
#   of the GaudiMM suite by external parallelization

#   https://github.com/insilichem/pgaudi

#   Copyright 2019 Andrés Giner Antón, Jaime Rodriguez-Guerra
#   and Jean-Didier Marechal

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#############

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
__url__ = "https://github.com/insilichem/pgaudi"
__title__ = "PGaudi"
__description__ = "A package for the optimization of the performance of the GaudiMM suite by external parallelization."
