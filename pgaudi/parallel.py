#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os
import io
import subprocess
import copy
import itertools
import similarity


def divide_cfg(cfg, processes):

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
    subprocess.call("gaudi run {}".format(in_file), shell=True)


def similarity_parallel(pair_list):
    pairs_selected = []
    for pair_indv in itertools.product(pair_list[0], pair_list[1]):
        test = similarity.rmsd(pair_indv[0], pair_indv[1], 0.5, ["Ligand"])
        if test == True:
            pairs_selected.append(pair_indv)
    return pairs_selected
