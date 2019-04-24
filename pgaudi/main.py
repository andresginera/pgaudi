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


def run(input_yaml, processes, complexity):
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

    # Load data input yaml file and generates the input cfgs
    if isinstance(input_yaml, basestring) and os.path.isfile(input_yaml):
        cfg = gaudi.parse.Settings(input_yaml)
    pcfg_names, pcfgs = parallel.divide_cfg(cfg, processes, complexity)

    # Parallelize gaudi process
    pool = multiprocessing.Pool(processes=processes)
    pool.map(parallel.gaudi_parallel, pcfg_names)

    for name in pcfg_names:
        os.remove(name)

    # Store all individuals in populations and merge them
    subpop = pool.map(treatment.parse_zip, [pcfg.output.path for pcfg in pcfgs])
    population = list(itertools.chain.from_iterable(subpop))

    # Delete double solutions
    print("\nRemoving double solutions...\n")
    combinations = list(itertools.combinations(subpop, 2))
    pool = multiprocessing.Pool(processes=len(combinations))
    pair_selected = pool.map(
        partial(parallel.similarity_parallel, cfg=cfg), combinations
    )
    similarity.remove_equal(pair_selected, population)

    # Creation of output files
    create_output.merge_log(pcfgs, cfg)
    create_output.generate_out(population, cfg)


def parse_cli():
    import argparse as arg

    parser = arg.ArgumentParser(
        prog="Pgaudi",
        usage="pgaudi filename [-p int] [-e] [-h]",
        description="Pgaudi is responsable of the optimization of the performance \
            of the GaudiMM suite by external parallelization",
    )
    parser.add_argument("filename", type=str, help="the YAML input file")
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
    return parser.parse_args()


def main():
    args = parse_cli()
    run(args.filename, args.processes, args.equal)


if __name__ == "__main__":
    main()

