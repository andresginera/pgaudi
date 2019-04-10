#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
# Python
import multiprocessing
import subprocess
import itertools
import os
import yaml

# Gaudi
import gaudi.parse

# Pgaudi
import parallel
import treatment
import similarity
import create_output


def main(input_yaml, processes=multiprocessing.cpu_count()):

    # Load data in input file yaml
    if isinstance(input_yaml, basestring) and os.path.isfile(input_yaml):
        cfg = gaudi.parse.Settings(input_yaml)

    # Divide input yaml files
    files, content = parallel.divide_cfg(cfg, processes)

    # Parallelize gaudi process
    pool = multiprocessing.Pool(processes=processes)
    pool.map(parallel.gaudi_parallel, files)

    group = []

    # Save the files in dictionaries (individuals) and save them in pop
    for con in content:
        treatment.descompress(con.output.path)
        group.append(treatment.store(con.output.path, con.ga.population))

    population = list(itertools.chain.from_iterable(group))

    # Delete double solutions
    combinations = list(itertools.combinations(group, 2))
    pool = multiprocessing.Pool(len(combinations))
    pair_selected = pool.starmap(parallel.similarity_parallel, (combinations))
    similarity.remove_equal(pair_selected, population)

    print(len(population))

    # Creation of output files
    create_output.merge_log(content, cfg)
    create_output.generate_out(population, cfg)


if __name__ == "__main__":
    import argparse as arg

    parser = arg.ArgumentParser(prog="ARGUMENTS", usage="%(prog)s [options]")
    parser.add_argument("yaml_file", type=str, help="The YAML input file")
    parser.add_argument(
        "number_processes",
        type=int,
        help="The number of processes in which the main process is divided",
    )
    args = parser.parse_args()
    main(str(args.yaml_file), int(args.number_processes))

