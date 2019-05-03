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
