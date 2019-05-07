FAQ
===

What license apply to PGaudi?
-----------------------------

PGaudi is a scientific software and is licensed under Apache License 2.0,
but includes work from other developers, whose licenses apply. Please check
the `LICENSE <https://github.com/andresginera/pgaudi/blob/master/LICENSE>`_ file in the root directory for further details.

.. _variables:

Which values for the variables of the GA do I set in the input file?
---------------------------------------------------------------------

These values are up to you. You can do several tries yourself to know the most optimal
values for your experiment. In the `GaudiMM's documentation <https://gaudi.readthedocs.io/en/latest/faq.html#how-many-generations-which-population-size-should-i-pick>`_ there is some
guidance that can help you too.

However, in PGaudi you have to take into account that the new subprocess are
simpler and some variables of the Genetical Algorithm are decreased. We
recommend as a first try a value of 25 generations and 50 individuals per
population per new subprocesses generated. So, depending on you number of
processes the configuration of these values in the input.yaml will be
different.


.. Note::
    You can extend this list with your questions in the `issues section. <https://github.com/andresginera/pgaudi/issues>`_
