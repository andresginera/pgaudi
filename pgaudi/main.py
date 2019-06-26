#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############
#   PGaudi: A package for optimize the performance
#   of the GaudiMM suite by external parallelization

#   https://github.com/insilichem/pgaudi

#   Copyright 2019 Andrés Giner Antón, Jaime Rodriguez-Guerra
#   and Jean-Didier Marechal

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#############

"""
Main module of the package from which the main process is run and the parallelization is controlled.
"""

from __future__ import absolute_import

# Imports
# Python
import sys
import os
import multiprocessing
import itertools
from functools import partial

# Gaudi
import gaudi.parse

# Pgaudi
from . import parallel, treatment, similarity, create_output


def run(cfg, processes, complexity):
    """
    Function that executes the whole job.

    Parameters
    ----------
    cfg : str or gaudi.parse.Settings
        Path to YAML input file or an already parsed YAML file
        via `gaudi.parse.Settings` class.
    processes : int
        Number of processes in which the main process is divided.
        Default = number of cores detected in the CPU's machine. 
    complexity : bool
        If True, the new subprocesses generated are computational
        equal to the main process.
        Default = False.

    """

    # Load data input yaml file and generates the input cfgs
    if isinstance(cfg, basestring) and os.path.isfile(cfg):
        cfg = gaudi.parse.Settings(cfg)
    pcfg_names, pcfgs = parallel.divide_cfg(cfg, processes, complexity)

    # Parallelize gaudi process
    pool = multiprocessing.Pool(processes=processes)
    try:
        pool.map_async(
            parallel.gaudi_parallel, pcfg_names, chunksize=1, callback=None
        ).get(9999999)
    except KeyboardInterrupt:
        pool.terminate()
        sys.exit("Exiting...")
    except Exception as e:
        print("An error ocurred:", type(e).__name__, e.message)
        pool.terminate()
    finally:
        pool.close()
        pool.join()

    for name in pcfg_names:
        os.remove(name)

    # Store all individuals in populations and merge them
    pool = multiprocessing.Pool(processes=processes)
    subpop = pool.map(treatment.parse_zip, [pcfg.output.path for pcfg in pcfgs])
    population = list(itertools.chain.from_iterable(subpop))

    # Delete double solutions
    print("\nRemoving double solutions...\n")
    combinations = list(itertools.combinations(subpop, 2))
    pool = multiprocessing.Pool(processes=len(combinations))
    pair_selected = pool.map(
        partial(parallel.similarity_parallel, cfg=cfg), combinations
    )
    clnpop = similarity.remove_equal(pair_selected, population)

    # Creation of output files
    create_output.merge_log(pcfgs, cfg)
    create_output.generate_out(clnpop, cfg)


def parse_cli():
    """
    Function to parse the arguments of the command line

    Returns
    -------
    args : argparse.Namespace
        List of the arguments gathered from the command line.

    """
    import argparse as arg

    # Customize banner and Usage message
    banner = '''
    \n    `7MM"""Yb.    .g8"""bgd       db   `7MMF'   `7MF'`7MM"""Yb. `7MMF'       
      MM    `Mb .dP'     `M      ;MM:    MM       M    MM    `Yb. MM        
      MM    ,MP dM'       `     ,V^MM.   MM       M    MM     `Mb MM        
      MMmmmdP"  MM             ,M  `MM   MM       M    MM      MM MM        
      MM        MM.    `7MMF'  AbmmmqMA  MM       M    MM     ,MP MM        
      MM        `Mb.     MM   A'     VML YM.     ,M    MM    ,dP' MM        
    .JMML.        `"bmmmdPY .AMA.   .AMMA.`bmmmmd"'  .JMMmmmdP' .JMML.      

    ==================================================================

    PGaudi is responsable of the optimization of the performance
    of the GaudiMM suite by external parallelization

    See also: https://github.com/andresginera/pgaudi\n
    '''

    class CapitalisedHelpFormatter(arg.HelpFormatter):
        def add_usage(self, usage, actions, groups, prefix=None):
            if prefix is None:
                prefix = banner
            return super(CapitalisedHelpFormatter, self).add_usage(
                usage, actions, groups, prefix
            )

    # Definining the program and the argument filename
    parser = arg.ArgumentParser(
        prog="pgaudi",
        add_help=False,
        formatter_class=CapitalisedHelpFormatter,
        usage="\nUsage: pgaudi <FILENAME> [-p PROCESSES] [-e] [-h] [-v]",
    )
    parser.add_argument(
        "filename", type=str, help="YAML input file.", metavar="Filename"
    )

    # Options
    parser.add_argument(
        "-p",
        metavar="<PROCESSES>",
        type=int,
        help="Number of processes in which the main process is divided. [Default = cores in this machine: {}]".format(
            multiprocessing.cpu_count()
        ),
        default=multiprocessing.cpu_count(),
    )
    parser.add_argument(
        "-e",
        "--equal",
        help="Set the new subprocesses generated computionally equal to the main process. [Default = False]",
        action="store_true",
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=arg.SUPPRESS,
        help="Show this help message and exit.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
        help="Show program's version number and exit.",
    )

    # Customing titles
    parser._positionals.title = "Arguments"
    parser._optionals.title = "Options"

    return parser.parse_args()


def main():
    """
    Main function that gathers the arguments from the command line with :func:`parse_cli()` and execute the function :func:`run()`.
    """
    args = parse_cli()
    run(args.filename, args.p, args.equal)


if __name__ == "__main__":
    main()

