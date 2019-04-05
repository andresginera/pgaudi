#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import subprocess
import parallel
import treatment
import similarity
import create_output
import itertools
import os
import yaml


def main(input_yaml, processes=multiprocessing.cpu_count()):

    # Load data in input file yaml
    with open(input_yaml, "r") as stream:
        data_loaded = yaml.load(stream)
    name = os.path.basename(data_loaded["output"]["name"])

    # Divide input yaml files
    parallel.manual_parallelize(input_yaml, processes)

    # Parallelize gaudi process
    pool = multiprocessing.Pool(processes=processes)
    yaml_files = subprocess.check_output("ls input_*.yaml", shell=True).split()
    pool.map(parallel.gaudi_parallel, yaml_files)

    # Remove yaml extra generated
    subprocess.call("rm input_?.yaml", shell=True)

    # Stored all the directories with output files
    dir_list = treatment.output()

    # Save the files in dictionaries (individuals) and save them in pop
    pop = []
    for directory in dir_list:
        pop.append(treatment.store_pop(directory, 30))

    # Delete double solutions
    combinations = list(itertools.combinations(pop, 2))
    pool = multiprocessing.Pool(len(combinations))
    pair_selected = pool.map(parallel.similarity_parallel, (combinations))
    full_pop = list(itertools.chain.from_iterable(pop))
    similarity.remove_equal(pair_selected, full_pop)

    # Creation of output files and moving of zip to directories according the process
    create_output.merge_log(name)
    create_output.generate_out(full_pop, name, input_yaml)
    create_output.moving_zip(dir_list)


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
    print str(args.number_processes)
    main(str(args.yaml_file), int(args.number_processes))

