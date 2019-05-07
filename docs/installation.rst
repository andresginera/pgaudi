Installation
==============

For the installation of PGaudi you need to have installed the `GaudiMM suite <https://github.com/insilichem/gaudi>`_
and the software `UCSF Chimera <https://www.cgl.ucsf.edu/chimera/>`_. If you have already them installed following
the GaudiMM's installation you have done most of the work until now!
You only need to install PGaudi with the pip installer:

.. code-block:: console

    (insilichem)$ pip install -i https://test.pypi.org/simple/ pgaudi

Complete installation
---------------------

In case you haven't them installed follow these instructions:

1.- Download the `latest stable copy of UCSF Chimera <http://www.cgl.ucsf.edu/chimera/download.html>`_ and install it with:

.. code-block:: console

    $ chmod +x chimera-*.bin && sudo ./chimera-*.bin

2.- Install `Miniconda Python 2.7 Distribution <https://docs.conda.io/en/latest/miniconda.html>`_ for your platform and install it with:

.. code-block:: console

    $ bash Miniconda2*.sh

3.- Install Gaudi with conda in a new environment called insilichem
(or whatever other name you prefer after the -n flag), using these
custom channels (-c flags):

.. code-block:: console

    $ conda create -n insilichem -c omnia -c salilab -c insilichem -c bioconda gaudi

4.- Activate the new environment as proposed:

.. code-block:: console

    $ source activate insilichem

5.- Install PGaudi with the pip installer inside the conda environment:

.. code-block:: console

    (insilichem)$ pip install -i https://test.pypi.org/simple/ pgaudi

6.-Check if the installation was right with the command:

.. code-block:: console

    (insilichem)$ pgaudi -h 

And you will get the next help text:

.. code-block:: text

        `7MM"""Yb.    .g8"""bgd       db   `7MMF'   `7MF'`7MM"""Yb. `7MMF       
          MM    `Mb .dP'     `M      ;MM:    MM       M    MM    `Yb. MM        
          MM    ,MP dM'       `     ,V^MM.   MM       M    MM     `Mb MM        
          MMmmmdP"  MM             ,M  `MM   MM       M    MM      MM MM        
          MM        MM.    `7MMF'  AbmmmqMA  MM       M    MM     ,MP MM        
          MM        `Mb.     MM   A'     VML YM.     ,M    MM    ,dP' MM        
        .JMML.        `"bmmmdPY .AMA.   .AMMA.`bmmmmd"'  .JMMmmmdP' .JMML.      

        ==================================================================

        PGaudi is responsable of the optimization of the performance
        of the GaudiMM suite by external parallelization

        See also: https://github.com/andresginera/pgaudi


    Usage: pgaudi <FILENAME> [-p PROCESSES] [-e] [-h] [-v]

    Arguments:
      Filename        YAML input file.

    Options:
      -p <PROCESSES>  Number of processes in which the main process is divided.
                      [Default = cores in this machine: 4]
      -e, --equal     Set the new subprocesses generated computionally equal to
                      the main process. [Default: False]
      -h, --help      Show this help message and exit.
      -v, --version   Show program's version number and exit.

.. warning:: 

    If you don't get the help text and instead you have the next error:

    .. code-block:: console

        libgfxinfo.so: undefined symbol: _ZN7pcrecpp2RE4InitERKSsPKNS_10RE_OptionsE

    It is due a problem with the installation of GaudiMM and Chimera-Conda. It is
    a known problem and is covered in the `Pychimera documentation. <https://pychimera.readthedocs.io/en/latest/faq.html#chimera-reports-problems-with-libgfxinfo-so-and-pcrecpp>`_