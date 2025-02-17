.. _output:

***********
Output file
***********

gprMax produces an output file that has the same name as the input file but with ``.out`` appended. The output file uses the widely-supported HDF5 (https://www.hdfgroup.org/HDF5/) format which was designed to store and organize large amounts of numerical data.


File structure
==============

The output file has the following HDF5 attributes at the root (``/``):

* ``Title`` is the title of the model
* ``Iterations`` is the number of iterations for the time window of the model
* ``dx, dy, dz`` is a tuple containing the spatial discretisation, i.e. :math:`\Delta x`, :math:`\Delta y`, :math:`\Delta z`
* ``dt`` is the time step of the model, i.e. :math:`\Delta t`
* ``srcsteps`` is the spatial increment used to move all sources between model runs.
* ``rxsteps`` is the spatial increment used to move all receivers between model runs.
* ``ntx`` is the total number of sources in the model.
* ``nrx`` is the total number of receievers in the model.

The output file contains HDF5 groups for sources (``txs``) and receivers (``rxs``). Within each group are further groups that correspond to individual sources, e.g. ``tx1``, ``tx2`` etc..., and receivers, e.g. ``rx1``, ``rx2`` etc...

.. code-block:: none

    /
        rxs/
            rx1/
                Position
                Ex
                Ey
                Ez
                Hx
                Hy
                Hz
            rx2/
                ...
        txs/
            tx1/
                Position
            tx2/
                ...

Within each individual ``rx`` group are the following datasets:

* ``Position`` is the x, y, z position (in metres) of the receiver in the model.
* ``Ex`` is an array containing the time history (for the model time window) of the values of the x component of the electric field at that receiver position.
* ``Ey`` is an array containing the time history (for the model time window) of the values of the y component of the electric field at that receiver position.
* ``Ez`` is an array containing the time history (for the model time window) of the values of the z component of the electric field at that receiver position.
* ``Hx`` is an array containing the time history (for the model time window) of the values of the x component of the magnetic field at that receiver position.
* ``Hy`` is an array containing the time history (for the model time window) of the values of the y component of the magnetic field at that receiver position.
* ``Hz`` is an array containing the time history (for the model time window) of the values of the z component of the magnetic field at that receiver position.

Within each individual ``tx`` group is the following dataset:

* ``Position`` is the x, y, z position (in metres) of the receiver in the model.


Viewing output
==============

There are a number of free tools available to read HDF5 files. Also MATLAB has high- and low-level functions for reading and writing HDF5 files, i.e. ``h5info`` and ``h5disp`` are useful for returning information and displaying the contents of HDF5 files respectively. gprMax includes some Python modules (in the ``tools`` package) to help you view output data:

A-scans
-------

* Plot A-scans using the Python module ``plot_hdf5_Ascan.py``. The module uses matplotlib to plot the time history for the electric and magnetic field components for all receivers in a model (each receiver gets a separate figure window). Usage (from the top-level gprMax directory) is: ``python -m tools.plot_hdf5_Ascan my_outputfile.out``.

* Plot A-scans using the MATLAB script ``plot_hdf5_Ascan.m``. The script plots the time history for the electric and magnetic field components for all receivers in a model (each receiver gets a separate figure window).

B-scans
-------

gprMax produces a separate output file for each trace (A-scan) in the B-scan.

* Combine the separate output files into one file using the Python module ``outputfiles_mergehdf5.py``. Usage (from the top-level gprMax directory) is: ``python -m tools.outputfiles_mergehdf5 basefilename modelruns``, where ``basefilename`` is the base name file of the output file series, e.g. for ``myoutput1.out``, ``myoutput2.out`` the base file name would be ``myoutput``, and ``modelruns`` is the number of output files to combine.
* Plot an image of the B-scan using the Python module ``plot_hdf5_Bscan.py``. Usage (from the top-level gprMax directory) is: ``python -m tools.plot_hdf5_Bscan my_outputfile.out field``, where ``field`` is the name of field to plot, e.g. ``Ex``, ``Ey`` or ``Ez``.


