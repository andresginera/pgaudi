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

import os
import zipfile
import yaml
import tempfile


def parse_zip(directory):
    """
    Function for parse the output zip files of gaudi and save
    them in individuals stored in a population.

    Parameters
    ----------
    directory : str
        Path to the directory where the output zip files are located.

    Returns
    -------
    population : list
        List of individuals represented in dictionaries.
        
    """

    tmpdir = tempfile.mkdtemp("gaudi")
    zipfiles = [f for f in os.listdir(directory) if f.endswith(".zip")]
    population = []

    for zipf in zipfiles:
        individual = {}
        zipref = zipfile.ZipFile(os.path.join(directory, zipf))
        tmp = os.path.join(tmpdir, os.path.splitext(zipf)[0])
        try:
            os.mkdir(tmp)
        except OSError:
            pass
        zipref.extractall(tmp)
        individual["name"] = os.path.join(os.path.basename(directory), zipf)
        for name in os.listdir(tmp):
            absname = os.path.join(tmp, name)
            if name.endswith(".mol2"):
                if "Protein" in name:
                    individual["Protein"] = absname
                elif "Metal" in name:
                    individual["Metal"] = absname
                elif "Ligand" in name:
                    individual["Ligand"] = absname
            elif name.endswith(".gaudi"):
                with open(absname, "r") as _gaudi:
                    individual["score"] = yaml.load(_gaudi)["score"]
        population.append(individual)
        zipref.close()

    return population
