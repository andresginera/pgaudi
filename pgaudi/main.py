#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main module of the package from which the main process is run and the parallelization is controlled.
"""

# Imports
# Python
import multiprocessing
import itertools
import os
import yaml
from functools import partial

# Gaudi
import gaudi.parse

# Pgaudi
import parallel
import treatment
import similarity
import create_output


def mksubpopulations(pcfgs):
    """
    Function for the creation of the subpopulations.

    Arguments
    ---------
    pcfgs : list
        A list with the contents of the gaudi.parse.Settings 
        of the new subprocess yaml file.
    
    Returns
    -------
    subpopulations : list
        A list of lists of individuals.

    """

    subpopulations = []

    for pcfg in pcfgs:
        pcfg.ga.population = treatment.descompress(pcfg.output.path)
        subpopulations.append(treatment.store(pcfg))

    return subpopulations


def main(input_yaml, processes, complexity):
    """
    Main function that controls the execution of the parallelization and all subfunctions.

    Arguments
    ---------
    input_yaml : str or gaudi.parse.Settings
        Path to YAML input file or an already parsed YAML file
        via gaudi.parse.Settings class.
    processes : int
        Number of processes in which the main process is divided.
        Default = number of cores detected in the CPU's machine. 
    complexity : bool
        If True, the new subprocesses generated are computational
        equal to the main process.

    """

    # Load data in input file yaml
    if isinstance(input_yaml, basestring) and os.path.isfile(input_yaml):
        cfg = gaudi.parse.Settings(input_yaml)

    # Divide input yaml files
    pcfg_names, pcfgs = parallel.divide_cfg(cfg, processes, complexity)

    # Parallelize gaudi process
    pool = multiprocessing.Pool(processes=processes)
    pool.map(parallel.gaudi_parallel, pcfg_names)

    for name in pcfg_names:
        os.remove(name)

    # Merge all subpopulations in a unique population
    subpopulations = mksubpopulations(pcfgs)
    population = list(itertools.chain.from_iterable(subpopulations))

    # Delete double solutions
    combinations = list(itertools.combinations(subpopulations, 2))
    pool = multiprocessing.Pool(processes=len(combinations))
    pair_selected = pool.map(
        partial(parallel.similarity_parallel, cfg=cfg), combinations
    )
    similarity.remove_equal(pair_selected, population)

    print("\nTotal population: " + str(len(population)))

    # Creation of output files
    create_output.merge_log(pcfgs, cfg)
    create_output.generate_out(population, cfg)


# Change this block to run the program with the arguments for the parallelization
# inside the yaml file and not in the command line
if __name__ == "__main__":
    import argparse as arg

    parser = arg.ArgumentParser(
        prog="Pgaudi",
        usage="python main.py yaml [-p int] [-e] [-h]",
        description="Pgaudi is responsable of the optimization of the performance \
            of the GaudiMM suite by external parallelization",
    )
    parser.add_argument("yaml", type=str, help="the YAML input file")
    parser.add_argument(
        "-p",
        "--processes",
        type=int,
        help="the number of processes in which the main process is divided",
        default=multiprocessing.cpu_count(),
    )
    parser.add_argument(
        "-e",
        "--equal",
        help="if set the new subprocesses are computionally equal",
        action="store_true",
    )
    args = parser.parse_args()
    main(args.yaml, args.processes, args.equal)

