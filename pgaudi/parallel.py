#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for helper function for the parallel process: similarity and gaudi run.
"""

import yaml
import os
import io
import subprocess
import copy
import itertools
import similarity


def divide_cfg(cfg, processes):
    """
    From the input cfg (gaudi.parse.Settings) create the new yaml file for the parallel execution.

    Parameters
    ----------
    cfg : gaudi.parse.Settings
        The input cfg load in the gaudi class gaudi.parse.Settings.
    processes : int
        Number of processes in which the main process is divided.
    
    Return
    ------
    yamls_name : list
        A list with the names of the new yaml files generated.
    yamls_data : list
        A list with the contents of the gaudi.parse.Settings of each new yaml file.

    """

    yamls_name = []
    yamls_data = []

    # Changes of values for the new yaml files
    cfg.ga.generations = cfg.ga.generations / processes
    cfg.ga.population = cfg.ga.population / processes

    for i in range(processes):

        cfgp = copy.deepcopy(cfg)
        cfgp.output.name += "_input{}".format(i)
        cfgp.output.path += "/input{}".format(i)
        cfgp._path = os.path.abspath("input_{}.yaml".format(i))
        if not os.path.isdir(cfgp.output.path):
            os.mkdir(cfgp.output.path)

        with io.open("input_{}.yaml".format(i), "w", encoding="utf8") as f:
            yaml.dump(cfgp, f, default_flow_style=False, allow_unicode=True)

        yamls_name.append("input_{}.yaml".format(i))
        yamls_data.append(cfgp)

    return yamls_name, yamls_data


def gaudi_parallel(in_file):
    """
    Helper function for parallel run of the gaudi run function in a bash terminal.

    Parameters
    ----------
    in_file : str
        Name of the input yaml file.

    """
    subprocess.call("gaudi run {}".format(in_file), shell=True)


def similarity_parallel(pair_list):
    # I have to get the arguments of the cfg.similarity.args for the function rmsd. 
    # Right now I have to put the arguments threshold and subject manually.
    """
    Helper function for parallel rmsd function to detect double solutions

    Parameters
    ----------
    pair_list : list
        List of two populations to compare all individuals of each population with the rest of individuals.

    Returns
    -------
    pairs_selected : list
        List of tuples of the pairs of identical individuals.

    """
    pairs_selected = []
    for pair_indv in itertools.product(pair_list[0], pair_list[1]):
        test = similarity.rmsd(pair_indv[0], pair_indv[1], 0.5, ["Ligand"])
        if test == True:
            pairs_selected.append(pair_indv)
    return pairs_selected
