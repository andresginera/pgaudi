#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
