#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os
import io
import subprocess
import copy
import itertools
import similarity


def manual_parallelize(yaml_file, processes):
    with open(yaml_file) as f:
        data_loaded = yaml.load(f)
    # Changes of values for the new yaml files
    data_loaded["ga"]["generations"] = data_loaded["ga"]["generations"] / processes
    data_loaded["ga"]["population"] = data_loaded["ga"]["population"] / processes

    for i in range(processes):

        data_process = copy.deepcopy(data_loaded)
        data_process["output"]["name"] += "_input{}".format(i)
        data_process["output"]["path"] += "_input{}".format(i)

        with io.open("input_{}.yaml".format(i), "w", encoding="utf8") as f:
            yaml.dump(data_process, f, default_flow_style=False, allow_unicode=True)


def gaudi_parallel(in_file):
    subprocess.call("gaudi run {}".format(in_file), shell=True)
    return 0


def similarity_parallel(pair_list):
    pairs_selected = []
    for pair_indv in itertools.product(pair_list[0], pair_list[1]):
        test = similarity.rmsd(pair_indv[0], pair_indv[1], 1.0, ["Metal"])
        if test == True:
            pairs_selected.append(pair_indv)
    return pairs_selected
