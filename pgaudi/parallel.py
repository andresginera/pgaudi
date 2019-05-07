#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for helper function for the parallel process: similarity and gaudi run.
"""

import os
import subprocess
import copy
import itertools
import similarity


def divide_cfg(cfg, processes, complexity):
    """
    From the input cfg (gaudi.parse.Settings) create the new yaml file for the parallel execution.

    Parameters
    ----------
    cfg : gaudi.parse.Settings
        The loaded input cfg in a ``gaudi.parse.Settings`` object.
    processes : int
        Number of processes in which the main process is divided.
    complexity : bool
        If True, the computational complexity of the new subprocess 
        will be the same as for the main process.
    
    Returns
    -------
    pcfg_names : `list`
        A list with the names of the new yaml files generated.
    pcfgs : list
        A list with the contents of the gaudi.parse.Settings of each new yaml file.

    """

    pcfg_names = []
    pcfgs = []

    # Simplification of values for the new yaml files
    if not complexity:
        cfg.ga.generations = cfg.ga.generations / processes
        cfg.ga.population = cfg.ga.population / processes

    # Mandatory changes of values for the new yaml files
    for i in range(processes):

        pcfg = copy.deepcopy(cfg)
        pcfg.output.name += "_input{}".format(i)
        pcfg.output.path += "/input{}".format(i)
        if not os.path.isdir(pcfg.output.path):
            os.mkdir(pcfg.output.path)

        with open("input_{}.yaml".format(i), "w") as f:
            f.write(pcfg.toYAML())

        pcfg_names.append("input_{}.yaml".format(i))
        pcfgs.append(pcfg)

    return pcfg_names, pcfgs


def gaudi_parallel(yaml):
    """
    Helper function for parallel run of the gaudi run function in a bash terminal.

    Parameters
    ----------
    yaml : str
        Name of the input yaml file.

    """

    subprocess.call("gaudi run {}".format(yaml), shell=True)


def similarity_parallel(pair_list, cfg):
    """
    Helper function for parallel rmsd function to detect double solutions.

    Parameters
    ----------
    pair_list : tuple
        Tuple of two populations to compare all individuals of each population with 
        the individuals of the other population.

    Returns
    -------
    pairs_selected : list
        List of tuples of the pairs of identical individuals.

    """

    pairs_selected = []
    for pair_indv in itertools.product(pair_list[0], pair_list[1]):
        if similarity.rmsd(
            pair_indv[0], pair_indv[1], *cfg.similarity.args, **cfg.similarity.kwargs
        ):
            pairs_selected.append(pair_indv)
    return pairs_selected
