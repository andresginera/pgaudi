#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import glob


def output():
    l = subprocess.check_output(
        "for i in *.zip; do unzip -qq $i -d ${i%%_???.zip} && LIST=${i%%_???.zip}:$LIST; done; echo $LIST",
        shell=True,
    )
    # subprocess.call("rm *.zip", shell=True)

    l = l.split(":")
    l.remove("\n")
    l = list(set(l))
    return l


def store_pop(directory, pop_parallel):
    pop = []
    for i in range(pop_parallel):
        indv = {}
        ind = glob.glob("{}/*_{:03d}_*.mol2".format(directory, i))
        indv["name"] = "{}_{:03d}".format(directory, i)
        indv["number"] = str(i).zfill(3)
        indv["process"] = directory
        for molecule in ind:
            if "Protein" in molecule:
                indv["Protein"] = os.path.abspath(molecule)
            if "Metal" in molecule:
                indv["Metal"] = os.path.abspath(molecule)
            if "Ligand" in molecule:
                indv["Ligand"] = os.path.abspath(molecule)
        pop.append(indv)
    return pop
