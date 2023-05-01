

Dice Roll Simulation Tutorial
=============================

In this tutorial, we'll demonstrate how to use the SimManager package to manage your simulation results and logs, along with Hydra for flexible configuration management.

Prerequisites
-------------

Before starting, ensure you have the following prerequisites:

1. The `SimManager` package installed (https://github.com/IGITUGraz/SimManager).
2. Set the ``RESULTS_ROOT_DIR`` environment variable to a directory that houses all your results (e.g., ``$HOME/RESULTS``).

Configuring Your Simulation
---------------------------

For each simulation, you should have the following:

1. Parameters in your ``config.yaml`` file.
2. The ``desc`` and ``index`` parameters specified on the command line.

The ``desc`` parameter is a description string (preferably without spaces) and the ``index`` parameter is an integer. These parameters will create a uniquely named directory in ``$RESULTS_ROOT_DIR/DiceRollSimulation``.

You can control the configuration options using the ``simman_config.yaml`` and ``loggers.yaml`` files.

Running Your Simulation
-----------------------

To run the simulation, use the following command:

.. code-block:: bash

   python bin/example.py desc=sample_run index=1

This command will create a directory with a unique name like ``$RESULTS_ROOT_DIR/DiceRollSimulation/desc-sample_run,seed-102,index-1/``. Within this directory, you'll find the ``data``, ``logs``, and ``simulation`` directories.

Note that all these directories are made unwritable to protect the data.

Running the Analysis
--------------------

Further analysis should store data in the ``results`` subdirectory. Check out the documentation of the SimManager package (https://github.com/IGITUGraz/SimManager) to see how to use the ``simmanager.paths`` object for managing paths within your simulation directories.

In the current example, use the ``analysis.py`` script to analyze the simulation data. It takes the ``--dir`` argument, which is used to create an ``output_paths`` object. The ``analysis_main`` function reads data and parameters from the main simulation, calculates the histogram of the generated dice rolls, and saves the plot in the results directory.

Command:

.. code-block:: bash

    python analysis.py --dir $RESULTS_ROOT_DIR/DiceRollSimulation/desc-sample_run,seed-102,index-1/

This will create a histogram plot in the results directory.

Summary
-------

In this tutorial, we demonstrated how to use SimManager and Hydra to manage your simulation results, logs, and configurations. By following these steps, you can create a well-organized and reproducible simulation setup.
