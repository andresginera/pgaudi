#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module to work with the files generated after the gaudi run sobprocesses
"""

import os
import glob
import zipfile
import yaml


def descompress(directory):
    """
    Function to descompress to zip files generated.

    Arguments
    ---------
    directory : str
        Path to the output zip files.

    """
    # subprocess.call("for ZIP in *.zip; do unzip -qq $i; done", shell=True)
    zipfiles = [f for f in os.listdir(directory) if f.endswith(".zip")]
    for zipf in zipfiles:
        zipref = zipfile.ZipFile(os.path.join(directory, zipf))
        zipref.extractall(directory)


def store(directory, population):
    """
    Function to save the individual in dictionaries with: the path to 
    the .mol2 molecule files, name of the individual and scores.

    Arguments
    ---------
    directory : str
        Path to the output descompressed files.

    population : int
        Number of ideal number of individual per population

    Returns
    -------
    pop : list
        List of dictionaries in which each element is an individual with the properties:
            - name
            - score
            - Protein
            - Metal (Optional)
            - Ligand (Optional)

    """
    pop = []
    for i in range(population):
        individual = {}
        molecules = glob.glob(os.path.join(directory, "*_{:03d}_*.mol2".format(i)))
        if not bool(molecules):
            continue
        _gaudi = glob.glob(os.path.join(directory, "*_{:03d}.gaudi".format(i)))
        with open(_gaudi[0], "r") as f:
            data = yaml.load(f)
            individual["score"] = data["score"]
        individual["name"] = "{}_{:03d}".format(directory, i)
        for molecule in molecules:
            if "Protein" in molecule:
                individual["Protein"] = os.path.abspath(molecule)
            if "Metal" in molecule:
                individual["Metal"] = os.path.abspath(molecule)
            if "Ligand" in molecule:
                individual["Ligand"] = os.path.abspath(molecule)
        pop.append(individual)
    return pop


# Implementation of the individual as a class

# class MyIndividual(object):
#     def __init__(self, _gaudi, directory, i):
#         self.molecules = {}
#         with open(_gaudi, "r") as f:
#             data_loaded = yaml.load(f)
#         if "Protein" in data_loaded:
#             self.molecules["Protein"] = os.path.join(directory, data_loaded["Protein"])
#         if "Ligand" in data_loaded:
#             self.molecules["Ligand"] = os.path.join(directory, data_loaded["Ligand"])
#         if "Metal" in data_loaded:
#             self.molecules["Metal"] = os.path.join(directory, data_loaded["Metal"])
#         self.name = "{}_{:03d}".format(directory, i)
#         self.number = i
#         self.score = data_loaded["score"]

# def store(directory, population):
#     pop = []
#     for i in range(population):
#         ind = glob.glob(os.path.join(directory, "*_{:03d}.gaudi".format(i)))
#         if not bool(ind):
#             continue
#         individual = MyIndividual(ind[0], directory, i)
#         pop.append(individual)
#     return pop
