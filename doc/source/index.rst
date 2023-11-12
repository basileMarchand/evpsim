.. evpsim documentation master file, created by
   sphinx-quickstart on Sun Oct 15 12:32:50 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ElastoViscoPlastic material SIMulator
=====================================

The evpsim module simulates elasto-visco-plastic mechanical behavior for a given loading path (strain/stress/mixed).

.. math::

   \sigma (t)  = \mathcal{A}\left( \Delta \varepsilon ; \Sigma ( \tau < t ) \right)

Simulation is performed at the scale of a single material point. 
It would be conceivable to couple the evpsim module with a finite element 
code for structural calculations, but this would require some work to reorganize the code, 
particularly in terms of memory management. 
What's more, it would still be prohibitively expensive in terms of calculation costs compared with a dedicated implementation.


.. toctree::
   :maxdepth: 2
   
   Theory <theory/index.rst>
   Usage <usage/index.rst>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
