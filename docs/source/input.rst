.. _commands:

*******************
Input file commands
*******************

An input file has to be supplied to gprMax which should contain all the necessary information to run a GPR model. The input file is an ASCII text file which can be prepared with any text editor or word-processing program. In the input file the hash character (``#``) is reserved and is used to denote the beginning of a command which will be passed to gprMax. The general syntax of commands is:

.. code-block:: none

    #command_name: parameter1 parameter2 parameter3 ...

A command and associated parameters should occupy a single line of the input file, and only one command per line is allowed. Hence, the first character of a line containing a command **must** be the hash character (``#``). If the line starts with **any other character** it is ignored by the program. Therefore, user comments or descriptions can be included in the input file. If a line starts with a hash character (``#``) the program will expect a valid command. If the name of the command is not correct the program will abandon execution and issue an error message. When a command requires more than one parameter then these should be separated using a white space character.

The order of commands in the input file is not important with the exception of object construction commands.

To describe the commands that can be used in the input file and their parameters the following conventions are used:

* ``f`` means a real number which can be entered using either a ``[.]`` separating the integral from the decimal part, e.g. 1.5, or in scientific notation, e.g. 15e-1 or 0.15e1.
* ``i`` means an integer number.
* ``c`` means a single character, e.g. ``y``.
* ``str`` means a string of characters with **no** white spaces in between, e.g ``sand``.
* ``file`` means a filename.
* ``[ ]`` square brackets are used to indicate optional parameters.

Unless otherwise specified, the SI system of units is used throughout gprMax:

* All parameters associated with simulated space (i.e. size of model, spatial increments, etc...) should be specified in **metres**.
* All parameters associated with time (i.e. total simulation time, time instants, etc...) should be specified in **seconds**.
* All parameters denoting frequency should be specified in **Hertz**.
* All parameters associated with spatial coordinates in the model should  be specified in **metres**. The origin of the coordinate system **(0,0)** is at the lower left corner of the model.

It is important to note that gprMax converts spatial and temporal parameters given in **metres** and **seconds** respectively to integer values corresponding to **FDTD cell coordinates** and **iteration number**. Therefore, rounding to the nearest integer number of the user defined values is performed.

The fundamental spatial and temporal discretization steps are denoted as :math:`\Delta x` , :math:`\Delta y`, :math:`\Delta z` and :math:`\Delta t` respectively.

The commands have been grouped into six categories:

* **Essential** - required to run any model, such as the domain size and spatial discretization
* **General** - provide further control over the model
* **Media** - used to introduce different materials into the model
* **Object construction** - used to build geometric shapes with different constitutive parameters
* **Excitation and output** - used to place source and output points in the model
* **PML** - provide advanced customisation and optimisation of the absorbing boundary conditions

Essential commands
==================

Most of the commands are optional but there are some essential commands which are necessary in order to construct any model. For example, none of the media and object commands are necessary to run a model. However, without specifying any objects in the model gprMax will simulate free space (air), which on its own, is not particularly useful for GPR modelling. If you have not specified a command which is essential in order to run a model, for example the size of the model, gprMax will terminate execution and issue an appropriate error message.

The essential commands are:

#domain:
--------

Allows you to specify the size of the model. The syntax of the command is:

.. code-block:: none

    #domain: f1 f2 f3

where ``f1 f2 f3`` are the size of the model in the x, y, and z directions respectively. For example to specify a 500 x 500 x 1000mm model use: ``#domain: 0.5 0.5 1.0``

#dx_dy_dz:
----------

Allows you to specify the discretization of space in the x , y and z directions respectively (i.e. :math:`\Delta x` , :math:`\Delta y`, :math:`\Delta z`). The syntax of the command is:

.. code-block:: none

    #dx_dy_dz: f1 f2 f3

where ``f1`` is the spatial step in the x direction (:math:`\Delta x`), ``f2`` is the spatial step in the y direction (:math:`\Delta y`) and ``f3`` is the spatial step in the z direction (:math:`\Delta z`). The spatial discretization controls the maximum permissible time step :math:`\Delta t` with which the solution advances in time in order to reach the required simulated time window. The relation between :math:`\Delta t` and :math:`\Delta x` , :math:`\Delta y`, :math:`\Delta z` is:

.. math:: \Delta t \leq \frac{1}{c\sqrt{\frac{1}{(\Delta x)^2}+\frac{1}{(\Delta y)^2}+\frac{1}{(\Delta z)^2}}},

where :math:`c` is the speed of light. In gprMax the equality is used to determine :math:`\Delta t` from :math:`\Delta x` , :math:`\Delta y`, and :math:`\Delta z`. Small values of :math:`\Delta x` , :math:`\Delta y`, and :math:`\Delta z` result in small values for :math:`\Delta t` which means more iterations in order to reach a given simulated time. However, it is important to note that the smaller the values of :math:`\Delta x` , :math:`\Delta y`, :math:`\Delta z` and :math:`\Delta t` are the more accurate your model will be. See the :ref:`guidance` section for tips on choosing a spatial discretisation.

#time_window:
-------------

Allows you to specify the total required simulated time. The syntax of the command is:

.. code-block:: none

    #time_window: f1

or

.. code-block:: none

    #time_window: i1

In the first case the ``f1`` parameter determines the required simulated time in seconds. For example, if you want to simulate a GPR trace of 20 nanoseconds then ``#time_window: 20e-9`` can be used. gprMax will perform the necessary number of iterations in order to reach the required simulated time. Alternatively, if the command is specified with an ``i1`` gprMax will interpret this value as a total number of iterations. Hence the command ``#time_window: 100`` means that 100 iterations will be performed. The number of iterations and the total simulated time window are related by:

.. math:: t_w = \Delta t × N_{it},

where :math:`t_w` is the time window in seconds, :math:`\Delta t` the time step, and :math:`N_{it}` the number of iterations. gprMax converts the specified time window in seconds to a number of iterations internally using the aforementioned equation. The result of the division is rounded to the nearest integer.


General commands
================

.. _python:

#python: and #end_python:
-------------------------

Allows you to write blocks of Python code between ``#python`` and ``#end_python`` in the input file. The code is executed when the input file is read by gprMax.

For example, to use Python to automatically generate repetitive geometry:

.. code-block:: none

    #python:
    for x in range(0, 8)
        print(’#cylinder: z 0.000 0.100 {} 0.050 0.005 pec’.format(0.020 + x * 0.020))
    #end_python:

You can access the following built-in constants from your Python code:

* ``c`` which is the speed of light in vacuum :math:`c=2.9979245 \times 10^8` m/s
* ``e0`` which is the permittivity of free space :math:`\epsilon_0=8.854187 \times 10^{-12}` F/m
* ``m0`` which is the permeability of free space :math:`\mu_0=1.256637 \times 10^{-6}` H/m
* ``z0`` which is the impedance of free space :math:`z_0=376.7303134` Ohms

You can access the following built-in variables from your Python code:

* ``current_model_run`` which is the current run number of the model that is been executed.
* ``number_model_runs`` which is the total number of runs specified when the model was initiatially executed.

For example, if you running a model multiple times, e.g. to generate a scan, you can use the syntax: ``python -m gprMax my_input_file -n number_of_model_runs``

You can also access the built-in library of antenna models. Currently models of antennas similar to Geophysical Survey Systems, Inc. (GSSI) (http://www.geophysical.com) 1.5 GHz (Model 5100) antenna, and MALA Geoscience (http://www.malags.com/) 1.2 GHz antenna are included. They can be accessed from within a block of Python code using: ``from user_libs.antennas import antenna_like_GSSI_1500`` or ``from user_libs.antennas import antenna_like_MALA_1200``.

For example, to use Python to include one of the antenna models from the built-in library at a location 0.125m, 0.094m, 0.100m (x,y,z) using a 1mm spatial resolution:

.. code-block:: none

    #python:
    from user_libs.antennas import antenna_like_GSSI_1500
    antenna_like_GSSI_1500(0.125, 0.094, 0.100, 0.001)
    #end_python:

#time_step_limit_type:
----------------------------

Allows you to choose whether to set the time step based on the 2D or 3D CFL condition. This command is useful when running a 2D model, i.e. when one dimension of the domain is one cell thick, because it allows the time step to be relaxed to the 2D CFL condition. The syntax of the command is:

.. code-block:: none

    #time_step_limit_type: str1

where ``str1`` can be either 2D or 3D.

#time_step_stability_factor:
----------------------------

Allows you to alter the value of the time step :math:`\Delta t` used by gprMax. gprMax uses the equality in the CFL condition, hence the maximum permissible time step. If a smaller time step is required then the syntax of the command is:

.. code-block:: none

    #time_step_stability_factor: f1

where ``f1`` can take values :math:`0 < \textrm{f1} \leq 1`. Then the actual time step used will be :math:`\textrm{f1} \times \Delta t`, where :math:`\Delta t` is calculated using the equality from the CFL condition.

#title:
-------

Allows you to include a title for your model. This title is saved in the output file(s). The syntax of the command is:

.. code-block:: none

    #title: str1

where ``str1`` can contain white space characters to separate individual words. The title has to be contained in a single line.

#messages:
----------

Allows you to control the amount of information displayed on screen when gprMax is run. The syntax of the command is:

.. code-block:: none

    #messages: c1

where ``c1`` can be either y (yes) or n (no) which turns on or off the messages on the screen. The default value is y. When messages are on, gprMax will display on the screen information the translation of space and time values to cell coordinates, iteration number, material parameters etc... This information can be useful for error checking.

#num_threads:
-----------------

Allows you to control how many OpenMP threads (usually the number of CPU cores available) are used when running the model. The most computationally intensive parts of gprMax, which are the FDTD solver loops, have been parallelised using OpenMP (http://openmp.org) which supports multi-platform shared memory multiprocessing. The syntax of the command is:

.. code-block:: none

    #num_threads: i1

where ``i1`` is the number of OpenMP threads to use. If ``#num_threads`` is not specified gprMax will firstly look to see if the environment variable ``OMP_NUM_THREADS`` exists, and if not will detect and use all available CPU cores on the machine.

.. _geometryview:

#geometry_view:
---------------

Allows you output to file(s) information about the geometry of model. The file(s) use the open source Visualization ToolKit (VTK) (http://www.vtk.org) format which can be viewed in many free readers, such as Paraview (http://www.paraview.org). The command can be used to create several 3D views of the model which are useful for checking that it has been constructed as desired. The syntax of the command is:

.. code-block:: none

    #geometry_view: f1 f2 f3 f4 f5 f6 f7 f8 f9 file1 c1

* ``f1 f2 f3`` are the lower left (x,y,z) coordinates of the volume of the geometry view in metres.
* ``f4 f5 f6`` are the upper right (x,y,z) coordinates of the volume of the geometry view in metres.
* ``f7 f8 f9`` are the spatial discretisation of the geometry view in metres. Typically these will be the same as the spatial discretisation of the model but they can be courser if desired.
* ``file1`` is the filename of the file where the geometry view will be stored.
* ``c1`` can be either n (normal) or f (fine) which specifies whether to output the geometry information on a per-cell basis (n) or a per-cell-edge basis (f). The fine mode should be reserved for viewing detailed parts of the geometry that occupy small volumes, as using this mode can generate geometry files with large file sizes.

.. tip::

    When you want to just check the geometry of your model, run gprMax using the optional command line argument ``--geometry-only``. This will build the model and produce any geometry view files, but will not run the simulation.

#snapshot:
----------

Allows you to obtain information about the electromagnetic fields within a volume of the model at a given time instant. The file(s) use the open source Visualization ToolKit (VTK) (http://www.vtk.org) format which can be viewed in many free readers, such as Paraview (http://www.paraview.org). The syntax of this command is:

.. code-block:: none

    #snapshot: f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 file1

or

.. code-block:: none

    #snapshot: f1 f2 f3 f4 f5 f6 f7 f8 f9 i1 file1

* ``f1 f2 f3`` are the lower left (x,y,z) coordinates of the volume of the snapshot in metres.
* ``f4 f5 f6`` are the upper right (x,y,z) coordinates of the volume of the snapshot in metres.
* ``f7 f8 f9`` are the spatial discretisation of the snapshot in metres.
* ``f10`` or ``i1`` are the snapshot time in seconds (float number) or the iteration number (integer number) respectively which denote the point in time at which the snapshot will be taken.
* ``file1`` is the filename of the file where the snapshot will be stored.

For example to save a snapshot of the electromagnetic fields in the model at a simulated time of 3 nanoseconds use: ``#snapshot: 0 0 0 1 1 1 0.1 0.1 0.1 3e-9 snap1``


.. _materials:

Media commands
==============

Built-in materials
------------------

gprMax has two builtin materials which can be used by specifying the identifiers ``pec`` and ``free_space``. These simulate a perfect electric conductor and air, i.e. a non-magnetic material with :math:`\epsilon_r = 1`, :math:`\sigma = 0`, respectively. Additionally the identifiers ``grass`` and ``water`` are currently reserved for internal use and should not be used unless you intentionally want to change their properties.

#material:
----------

Allows you to introduce a material into the model described by a set of constitutive parameters. The syntax of the command is:

.. code-block:: none

    #material: f1 f2 f3 f4 str1

* ``f1`` is the relative permittivity, :math:`\epsilon_r`
* ``f2`` is the conductivity (Siemens/metre), :math:`\sigma`
* ``f3`` is the relative permeability, :math:`\mu_r`
* ``f4`` is the magnetic conductivity, :math:`\sigma_*`
* ``str1`` is an identifier for the material.

For example ``#material: 3 0.01 1 0 my_sand`` creates a material called ``my_sand`` which has a relative permittivity (frequency independent) of :math:`\epsilon_r = 3`, a conductivity of :math:`\sigma = 0.01` S/m, and is non-magnetic, i.e. :math:`\mu_r = 1` and :math:`\sigma_* = 0`


#add_dispersion_debye:
----------------------

Allows you to add dispersive properties to an already defined ``#material`` based on a multiple pole Debye formulation (see :ref:`capabilities` section). The syntax of the command is:

.. code-block:: none

    #add_dispersion_debye: i1 f1 f2 f3 f4 ... str1

* ``i1`` is the number of Debye poles.
* ``f1`` is the difference between the DC (static) relative permittivity and the relative permittivity at infinite frequency, i.e. :math:`\Delta \epsilon_r = \epsilon_{rs} - \epsilon_{r \infty}` , for the first Debye pole.
* ``f2`` is the relaxation time (seconds), :math:`\tau`, for the first Debye pole.
* ``f3`` is the difference between the DC (static) relative permittivity and the relative permittivity at infinite frequency, i.e. :math:`\Delta \epsilon_r = \epsilon_{rs} - \epsilon_{r \infty}` , for the second Debye pole.
* ``f4`` is the relaxation time (seconds), :math:`\tau`, for the second Debye pole.
* ``str1`` identifies the material to add the dispersive properties to.

For example to create a model of water with a single Debye pole, :math:`\epsilon_{rs} = 80.1`, :math:`\epsilon_{r \inf} = 4.9` and :math:`\tau = 9.231\times 10^{-12}` seconds use: ``#material: 4.9 0.0 1.0 0.0 my_water`` and ``#add_dispersion_debye: 1 75.2 9.231e-12 my_water``.

Important notes:

* You can continue to add pairs of values for :math:`\Delta \epsilon_r` and :math:`\tau` for as many Debye poles as you have specified with ``i1``.
* The relative permittivity in the ``#material`` command should be given as the relative permittivity at infinite frequency, i.e. :math:`\epsilon_{r \infty}`.
* Values for the relaxation times should always be greater than the time step :math:`\Delta t` used in the model. gprMax checks and verifies this condition and if it does not then will exit raising an error.


#add_dispersion_lorenz:
-----------------------

Allows you to add dispersive properties to an already defined ``#material`` based on a multiple pole Lorenz formulation (see :ref:`capabilities` section). The syntax of the command is:

.. code-block:: none

    #add_dispersion_lorenz: i1 f1 f2 f3 f4 f5 f6 ... str1

* ``i1`` is the number of Lorenz poles.
* ``f1`` is the difference between the DC (static) relative permittivity and the relative permittivity at infinite frequency, i.e. :math:`\Delta \epsilon_r = \epsilon_{rs} - \epsilon_{r \infty}` , for the first Lorenz pole.
* ``f2`` is the relaxation time (seconds), :math:`\tau`, for the first Lorenz pole.
* ``f3`` is the damping factor for the first Lorenz pole.
* ``f4`` is the difference between the DC (static) relative permittivity and the relative permittivity at infinite frequency, i.e. :math:`\Delta \epsilon_r = \epsilon_{rs} - \epsilon_{r \infty}` , for the second Lorenz pole.
* ``f5`` is the relaxation time (seconds), :math:`\tau`, for the second Lorenz pole.
* ``f6`` is the damping factor for the second Lorenz pole.
* ``str1`` identifies the material to add the dispersive properties to.

*For example...*

Important notes:

* You can continue to add triplets of values for :math:`\Delta \epsilon_r` and :math:`\tau` for as many Lorenz poles as you have specified with ``i1``.
* The relative permittivity in the ``#material`` command should be given as the relative permittivity at infinite frequency, i.e. :math:`\epsilon_{r \infty}`.
* Values for the relaxation times should always be greater than the time step :math:`\Delta t` used in the model. gprMax checks and verifies this condition and if it does not then will exit raising an error.


#add_dispersion_drude:
----------------------

Allows you to add dispersive properties to an already defined ``#material`` based on a multiple pole Drude formulation (see :ref:`capabilities` section). The syntax of the command is:

.. code-block:: none

    #add_dispersion_drude: i1 f1 f2 f3 f4 f5 f6 ... str1

* ``i1`` is the number of Drude poles.
* ``f1`` is the difference between the DC (static) relative permittivity and the relative permittivity at infinite frequency, i.e. :math:`\Delta \epsilon_r = \epsilon_{rs} - \epsilon_{r \infty}` , for the first Drude pole.
* ``f2`` is the relaxation time (seconds), :math:`\tau`, for the first Drude pole.
* ``f3`` is the **x** for the first Drude pole.
* ``f4`` is the difference between the DC (static) relative permittivity and the relative permittivity at infinite frequency, i.e. :math:`\Delta \epsilon_r = \epsilon_{rs} - \epsilon_{r \infty}` , for the second Drude pole.
* ``f5`` is the relaxation time (seconds), :math:`\tau`, for the second Drude pole.
* ``f6`` is the **x** for the second Drude pole.
* ``str1`` identifies the material to add the dispersive properties to.

*For example...*

Important notes:

* You can continue to add triplets of values for :math:`\Delta \epsilon_r` and :math:`\tau` for as many Drude poles as you have specified with ``i1``.
* The relative permittivity in the ``#material`` command should be given as the relative permittivity at infinite frequency, i.e. :math:`\epsilon_{r \infty}`.
* Values for the relaxation times should always be greater than the time step :math:`\Delta t` used in the model. gprMax checks and verifies this condition and if it does not then will exit raising an error.


#soil_peplinski:
----------------

Allows you to use a mixing model for soils proposed by Peplinski (http://dx.doi.org/10.1109/36.387598). The command is designed to be used in conjunction with the ``#fractal_box`` command for creating soils with realistic dielectric and geometric properties. The syntax of the command is:

.. code-block:: none

    #soil_peplinski: f1 f2 f3 f4 f5 f6 str1

* ``f1`` is the sand fraction of the soil.
* ``f2`` is the clay fraction of the soil.
* ``f3`` is the bulk density of the soil in grams per centimetre cubed.
* ``f4`` is the density of the sand particles in the soil in grams per centimetre cubed.
* ``f5`` and ``f6`` define a range for the volumetric water fraction of the soil.
* ``str1`` is an identifier for the soil.

For example for a soil with sand fraction 0.5, clay fraction 0.5, bulk density :math:`2~g/cm^3`, sand particle density of :math:`2.66~g/cm^3`, and a volumetric water fraction range of 0.001 - 0.25 use: ``#soil_peplinski: 0.5 0.5 2.0 2.66 0.001 0.25 my_soil``.

Object construction commands
============================

Object construction commands are processed in the order they appear in the input file. Therefore space in the model allocated to a specific material using for example the ``#box`` command can be reallocated to another material using the same or any other object construction command. Space in the model can be regarded as a canvas in which objects are introduced and one can be overlaid on top of the other overwriting its properties in order to produce the desired geometry. The object construction commands can therefore be used to create complex shapes and configurations.

Anisotropy
----------

It is possible to specify objects that have diagonal anisotropy which allows materials such as wood and fibre-reinforced composites, often imaged with GPR, to be more accurately modelled.

.. math::

    \bar{\bar{\epsilon}} = \left[ \begin{array}{ccc}
    \epsilon_{xx} & 0 & 0 \\
    0 & \epsilon_{yy} & 0 \\
    0 & 0 & \epsilon_{zz}
    \end{array} \right],\quad
    \bar{\bar{\sigma}}= \left[ \begin{array}{ccc}
    \sigma_{xx} & 0 & 0 \\
    0 & \sigma_{yy} & 0 \\
    0 & 0 & \sigma_{zz}
    \end{array} \right]

Standard isotropic objects specify one material identifier that defines the same properties in x, y, and z directions. However, every volumetric object building command can also be specified with three material identifiers, which allows properties for the x, y, and z directions to be separately defined. The ``#plate`` command, which defines a surface, can specify up to two material identifiers, and the ``#edge`` command, which defines a line, continues to take one material identifier. For example to create a box with different material properties in each of the x, y, and z directions use:

.. code-block:: none

    #material: 41 10 1 0 matX
    #material: 35 10 1 0 matY
    #material: 33 1 1 0 matZ
    #box: 0 0 0 0.1 0.1 0.1 matX matY matZ

As another example, to create a cylinder of radius 10 mm that has the same properties in the x and y directions but different properties in the z direction use:

.. code-block:: none

    #material: 41 10 1 0 matXY
    #material: 33 1 1 0 matZ
    #cylinder: 0.1 0.1 0.1 0.5 0.1 0.1 0.01 matXY matXY matZ


Dielectric smoothing
--------------------

At the boundaries between different materials in the model there is the question of which material properties to use. Should the last object to be defined at that location dictate the properties? Should an average set of properties of the materials of the objects that share that location be used? This latter option is often referred to as dielectric smoothing. To address this question gprMax includes an option to turn dielectric smoothing on or off for volumetric object building commands. The default behaviour (if no option is specified) is for dielectric smoothing to be on. The option can be specified with a single character ``y`` (on) or ``n`` (off) given after the material identifier in each object command. For example to specify a sphere of material ``sand`` with dielectric smoothing turned off use: ``#sphere: 0.5 0.5 0.5 0.1 sand n``.

Important notes:

* If an object is anistropic then dielectric smoothing is automatically turned off for that object.
* Non-volumetric object building commands, ``#edge`` and ``#plate`` cannot have dielectric smoothing.

#edge:
------

Allows you to introduce a wire with specific properties into the model. A wire is an edge of a Yee cell and it can be useful to model resistors or thin wires. The syntax of the command is:

.. code-block:: none

    #edge: f1 f2 f3 f4 f5 f6 str1

* ``f1 f2 f3`` are the starting (x,y,z) coordinates of the edge, and ``f4 f5 f6`` are the ending (x,y,z) coordinates of the edge. The coordinates should define a single line.
* ``str1`` is a material identifier that must correspond to material that has already been defined in the input file, or is one of the builtin materials ``pec`` or ``free_space``.

For example to specify a x-directed wire that is a perfect electric conductor, use: ``#edge: 0.5 0.5 0.5 0.7 0.5 0.5 pec``. Note that the y and z coordinates are identical.

#plate:
-------

Allows you to introduce a plate with specific properties into the model. A plate is a surface of a Yee cell and it can be useful to model objects thinner than a Yee cell. The syntax of the command is:

.. code-block:: none

    #plate: f1 f2 f3 f4 f5 f6 str1

* ``f1 f2 f3`` are the lower left (x,y,z) coordinates of the plate, and ``f4 f5 f6`` are the upper right (x,y,z) coordinates of the plate. The coordinates should define a surface and not a 3D object like the ``#box`` command.
* ``str1`` is a material identifier that must correspond to material that has already been defined in the input file, or is one of the builtin materials ``pec`` or ``free_space``.

For example to specify a xy oriented plate that is a perfect electric conductor, use: ``#plate: 0.5 0.5 0.5 0.7 0.8 0.5 pec``. Note that the z coordinates are identical.

#triangle:
----------

Allows you to introduce a triangular patch or a triangular prism with specific properties into the model. The patch is just a triangular surface made as a collection of staircased Yee cells, and the triangular prism extends the triangular patch in the direction perpendicular to the plane. The syntax of the command is:

.. code-block:: none

    #triangle: f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 str1

* ``f1 f2 f3`` are the coordinates (x,y,z) of the first apex of the triangle, ``f4 f5 f6`` the coordinates (x,y,z) of the second apex, and ``f7 f8 f9`` the coordinates (x,y,z) of the third apex.
* ``f10`` is the thickness of the triangular prism. If the thickness is zero then a triangular patch is created.
* ``str1`` is a material identifier that must correspond to material that has already been defined in the input file, or is one of the builtin materials ``pec`` or ``free_space``.

For example, to specify a xy orientated triangular patch that is a perfect electric conductor, use: ``#triangle: 0.5 0.5 0.5 0.6 0.4 0.5 0.7 0.9 0.5 0.0 pec``. Note that the z coordinates are identical and the thickness is zero.

#box:
-----

Allows you to introduce an orthogonal parallelepiped with specific properties into the model. The syntax of the command is:

.. code-block:: none

    #box: f1 f2 f3 f4 f5 f6 str1

* ``f1 f2 f3`` are the lower left (x,y,z) coordinates of the parallelepiped, and ``f4 f5 f6`` are the upper right (x,y,z) coordinates of the parallelepiped.
* ``str1`` is a material identifier that must correspond to material that has already been defined in the input file, or is one of the builtin materials ``pec`` or ``free_space``.

#sphere:
--------

Allows you to introduce a spherical object with specific parameters into the model. The syntax of the command is:

.. code-block:: none

    #sphere: f1 f2 f3 f4 str1

* ``f1 f2 f3`` are the coordinates (x,y,z) of the centre of the sphere.
* ``f4`` is its radius.
* ``str1`` is a material identifier that must correspond to material that has already been defined in the input file, or is one of the builtin materials ``pec`` or ``free_space``.

For example, to specify a sphere with centre at (0.5, 0.5, 0.5), radius 100 mm, and with constitutive parameters of ``my_sand``, use: ``#sphere: 0.5 0.5 0.5 0.1 my_sand``.

Important notes:

* Sphere objects are permitted to extend outwith the model domain if desired, however, only parts of object inside the domain will be created.

#cylinder:
----------

Allows you to introduce a circular cylinder into the model. The orientation of the cylinder axis can be arbitrary, i.e. it does not have align with one of the Cartesian axes of the model. The syntax of the command is:

.. code-block:: none

    #cylinder: f1 f2 f3 f4 f5 f6 f7 str1

* ``f1 f2 f3`` are the coordinates (x,y,z) of the centre of one face of the cylinder, and ``f4 f5 f6`` are the coordinates (x,y,z) of the centre of the other face.
* ``f7`` is the radius of the cylinder.
* ``str1`` is a material identifier that must correspond to material that has already been defined in the input file, or is one of the builtin materials ``pec`` or ``free_space``.

For example, to specify a cylinder with its axis in the y direction, a length of 0.7 m, a radius of 100 mm, and that is a perfect electric conductor, use: ``#cylinder: 0.5 0.1 0.5 0.5 0.8 0.5 0.1 pec``.

Important notes:

* Cylinder objects are permitted to extend outwith the model domain if desired, however, only parts of object inside the domain will be created.


#cylindrical_sector:
--------------------

Allows you to introduce a cylindrical sector (shaped like a slice of pie) into the model. The syntax of the command is:

.. code-block:: none

    #cylindrical_sector: c1 f1 f2 f3 f4 f5 f6 f7 str1

* ``c1`` is the direction of the axis of the cylinder from which the sector is defined and can be ``x``, ``y``, or ``z``.
* ``f1 f2`` are the coordinates of the centre of the cylindrical sector.
* ``f3 f4`` are the lower and higher coordinates of the axis of the cylinder from which the sector is defined (in effect they specify the thickness of the sector).
* ``f5`` is the radius of the cylindrical sector.
* ``f6`` is the starting angle (in degrees) for the cylindrical sector (with zero degrees defined on the positive first axis of the plane of the cylindrical sector).
* ``f7`` is the angle (in degrees) swept by the cylindrical sector (the finishing angle of the sector is always anti-clockwise from the starting angle).
* ``str1`` is a material identifier that must correspond to material that has already been defined in the input file, or is one of the builtin materials ``pec`` or ``free_space``.

For example, to specify a cylindrical sector with its axis in the z direction, radius of 0.25 m, thickness of 2 mm, a starting angle of 330 :math:`^\circ`, a sector angle of 60 :math:`^\circ`, and that is a perfect electric conductor, use: ``#cylindrical_sector: z 0.34 0.24 0.500 0.502 0.25 330 60 pec``.

Important notes:

* Cylindrical sector objects are permitted to extend outwith the model domain if desired, however, only parts of object inside the domain will be created.

.. _fractals:

#fractal_box:
-------------

Allows you to introduce an orthogonal parallelepiped with fractal distributed properties which are related to a mixing model or normal material into the model. The syntax of the command is:

.. code-block:: none

    #fractal_box: f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 i1 str1 str2 [i2]

* ``f1 f2 f3`` are the lower left (x,y,z) coordinates of the parallelepiped, and ``f4 f5 f6`` are the upper right (x,y,z) coordinates of the parallelepiped.
* ``f7`` is the fractal dimension which, for an orthogonal parallelepiped, should take values between zero and three.
* ``f8`` is used to weight the fractal in the x direction.
* ``f9`` is used to weight the fractal in the y direction.
* ``f10`` is used to weight the fractal in the z direction.
* ``i1`` is the number of materials to use for the fractal distribution (defined according to the associated mixing model). This should be set to one if using a normal material instead of a mixing model.
* ``str1`` is an identifier for the associated mixing model or material.
* ``str2`` is an identifier for the fractal box itself.
* ``i2`` is an optional parameter which controls the seeding of the random number generator used to create the fractals. By default (if you don't specify this parameter) the random number generator will be seeded by trying to read data from ``/dev/urandom`` (or the Windows analogue) if available or from the clock otherwise.

For example, to create an orthogonal parallelepiped with fractal distributed properties using a Peplinski mixing model for soil, with 50 different materials over a range of water volumetric fractions from 0.001 - 0.25, you should first define the mixing model using: ``#soil_peplinski: 0.5 0.5 2.0 2.66 0.001 0.25 my_soil`` and then specify the fractal box using ``#fractal_box: 0 0 0 0.1 0.1 0.1 1.5 1 1 1 50 my_soil my_fractal_box``.

#add_surface_roughness:
-----------------------

Allows you to add rough surfaces to a ``#fractal_box`` in the model. A fractal distribution is used for the profile of the rough surface. The syntax of the command is:

.. code-block:: none

    #add_surface_roughness: f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 str1 [i1]

* ``f1 f2 f3`` are the lower left (x,y,z) coordinates of a surface on a ``#fractal_box``, and ``f4 f5 f6`` are the upper right (x,y,z) coordinates of a surface on a ``#fractal_box``. The coordinates must locate one of the six surfaces of a ``#fractal_box`` but do not have to extend over the entire surface.
* ``f7`` is the fractal dimension which, for an orthogonal parallelepiped, should take values between zero and three.
* ``f8`` is used to weight the fractal in the first direction of the surface.
* ``f9`` is used to weight the fractal in the second direction of the surface.
* ``f10 f11`` define lower and upper limits for a range over which the roughness can vary. These limits should be specified relative to the dimensions of the ``#fractal_box`` that the rough surface is being applied.
* ``str1`` is an identifier for the ``#fractal_box`` that the rough surface should be applied to.
* ``i1`` is an optional parameter which controls the seeding of the random number generator used to create the fractals. By default (if you don't specify this parameter) the random number generator will be seeded by trying to read data from ``/dev/urandom`` (or the Windows analogue) if available or from the clock otherwise.

Up to six ``#add_rough_surface commands`` can be given for any ``#fractal_box`` corresponding to the six surfaces.

For example, if a ``#fractal_box`` has been specified using: ``#fractal_box: 0 0 0 0.1 0.1 0.1 1.5 1 1 1 50 my_soil my_fractal_box`` then to apply a rough surface that varys between 85 mm and 110 mm (i.e. valleys that are up to 15 mm deep and peaks that are up to 10 mm tall) to the surface that is in the positive z direction, use ``#add_surface_roughness: 0 0 0.1 0.1 0.1 0.1 1.5 1 1 0.085 0.110 my_fractal_box``.

#add_surface_water:
-------------------

Allows you to add surface water to a ``#fractal_box`` in the model that has had a rough surface applied. The syntax of the command is:

.. code-block:: none

    #add_surface_water: f1 f2 f3 f4 f5 f6 f7 str1

* ``f1 f2 f3`` are the lower left (x,y,z) coordinates of a surface on a ``#fractal_box``, and ``f4 f5 f6`` are the upper right (x,y,z) coordinates of a surface on a ``#fractal_box``. The coordinates must locate one of the six surfaces of a ``#fractal_box`` but do not have to extend over the entire surface.
* ``f7`` defines the depth of the water, which should be specified relative to the dimensions of the ``#fractal_box`` that the surface water is being applied.
* ``str1`` is an identifier for the ``#fractal_box`` that the surface water should be applied to.

For example, to add surface water that is 5 mm deep to an existing ``#fractal_box`` that has been specified using ``#fractal_box: 0 0 0 0.1 0.1 0.1 1.5 1 1 1 50 my_soil my_fractal_box`` and has had a rough surface applied using ``#add_surface_roughness: 0 0 0.1 0.1 0.1 0.1 1.5 1 1 0.085 0.110 my_fractal_box``, use ``#add_surface_water: 0 0 0.1 0.1 0.1 0.1 0.105 my_fractal_box``.

Important notes:

* The water is modelled using a single-pole Debye formulation with properties :math:`\epsilon_{rs} = 80.1`, :math:`\epsilon_{\infty} = 4.9`, and a relaxation time of :math:`\tau = 9.231 \times 10^{-12}` seconds (http://dx.doi.org/10.1109/TGRS.2006.873208). If you prefer, gprMax will use your own definition for water as long as it is named ``water``.

#add_grass:
-----------

Allows you to add grass with roots to a ``#fractal_box`` in the model. The blades of grass are randomly distributed over the specified surface area and a fractal distribution is used to vary the height of the blades of grass and depth of the grass roots. The syntax of the command is:

.. code-block:: none

    #add_grass: f1 f2 f3 f4 f5 f6 f7 f8 f9 i1 str1 [i2]

* ``f1 f2 f3`` are the lower left (x,y,z) coordinates of a surface on a ``#fractal_box``, and ``f4 f5 f6`` are the upper right (x,y,z) coordinates of a surface on a ``#fractal_box``. The coordinates must locate one of three surfaces (in the positive axis direction) of a ``#fractal_box`` but do not have to extend over the entire surface.
* ``f7`` is the fractal dimension which, for an orthogonal parallelepiped, should take values between zero and three.
* ``f8 f9`` define lower and upper limits for a range over which the height of the blades of grass can vary. These limits should be specified relative to the dimensions of the ``#fractal_box`` that the grass is being applied.
* ``i1`` is the number of blades of grass that should be applied to the surface area.
* ``str1`` is an identifier for the ``#fractal_box`` that the grass should be applied to.
* ``i2`` is an optional parameter which controls the seeding of the random number generator used to create the fractals. By default (if you don't specify this parameter) the random number generator will be seeded by trying to read data from ``/dev/urandom`` (or the Windows analogue) if available or from the clock otherwise.

For example, to apply 100 blades of grass that vary in height between 100 and 150 mm to the entire surface in the positive z direction of a ``#fractal_box`` that had been specified using ``#fractal_box: 0 0 0 0.1 0.1 0.1 1.5 1 1 50 my_soil my_fractal_box``, use: ``#add_grass: 0 0 0.1 0.1 0.1 0.1 1.5 0.2 0.25 100 my_fractal_box``.

Important notes:

* The grass is modelled using a single-pole Debye formulation with properties :math:`\epsilon_{rs} = 18.5087`, :math:`\epsilon_{\infty} = 12.7174`, and a relaxation time of :math:`\tau = 1.0793 \times 10^{-11}` seconds (http://dx.doi.org/10.1007/BF00902994). If you prefer, gprMax will use your own definition for grass if you use a material named ``grass``. The geometry of the blades of grass are defined by the parametric equations: :math:`x = x_c +s_x {\left( \frac{t}{b_x} \right)}^2`, :math:`y = y_c +s_y {\left( \frac{t}{b_y} \right)}^2`, and :math:`z=t`, where :math:`s_x` and :math:`s_y` can be -1 or 1 which are randomly chosen, and where the constants :math:`b_x` and :math:`b_y` are random numbers based on a Gaussian distribution.

Excitation commands
===================

#waveform:
----------

Allows you to specify waveforms to use with sources in the model. The syntax of the command is:

.. code-block:: none

    #waveform: str1 f1 f2 str2

* ``str1`` is the type of waveform which can be:

    * ``gaussian`` which is a Gaussian waveform.
    * ``gaussiandot`` which is the first derivative of a Gaussian waveform.
    * ``gaussiandotnorm`` which is the normalised first derivative of a Gaussian waveform.
    * ``gaussiandotdot`` which is the second derivative of a Gaussian waveform.
    * ``gaussiandotdotnorm`` which is the normalised second derivative of a Gaussian waveform.
    * ``gaussiandotdotdot`` which is the third derivative of a Gaussian waveform.
    * ``ricker`` which is a Ricker (or Mexican hat) waveform, i.e. the negative, normalised second derivative of a Gaussian waveform.
    * ``sine`` which is a single cycle of a sine waveform.
    * ``contsine`` which is a continuous sine waveform. In order to avoid introducing noise into the calculation the amplitude of the waveform is modulated for the first cycle of the sine wave (ramp excitation).
* ``f1`` is the amplitude of the waveform.
* ``f2`` is the frequency of the waveform in Hertz.
* ``str2`` is an identifier for the waveform used to assign it to a source.

For example, to specify a Gaussian waveform with an amplitude of one and a centre frequency of 1.2 GHz, use: ``#waveform: gaussian 1 1.2e9 my_gauss_pulse``.

Important notes:

* The functions used to create the waveforms can be found in the :ref:`waveforms` appendix.

#excitation_file:
-----------------

Allows you to specify an ASCII file that contains columns of amplitude values that specify custom waveform shapes that can be used with sources in the model. The first row of each column must begin with a identifier string that will be used as the name of each waveform. There needs to be at least as many amplitude values as the number of iterations that are going to be performed. If there are less than this number then at the end of the sequence of amplitude values zero values will be added to pad the sequence up to the number of iterations. If extra amplitude values are specified than needed then they are ignored. The syntax of the command is:

.. code-block:: none

    #excitation_file: file1

``str1`` is the name of the ASCII file containing the specified waveform. It should be located in the same directory as the input file.

For example, to specify the file ``my_waves.txt``, which contains two custom waveform shapes, use: ``#excitation_file: my_waves.txt``. The contents of the file ``my_waves.txt`` would take the form:

.. code-block:: none

    my_pulse1    my_pulse2
    0           0
    1.2e-6      0
    1.3e-6      1e-1
    5e-6        1.5e-1
    ...         ...
    ...         ...
    ...         ...

#hertzian_dipole:
-----------------

Allows you to specify a current density term at an electric field location (the simplest excitation). This will simulate an infinitesimal electric dipole (it does have a length of :math:`\Delta l`). This is often referred to as an additive or soft source. The syntax of the command is:

.. code-block:: none

    #hertzian_dipole: c1 f1 f2 f3 [f4 f5] str1

* ``c1`` is the polarisation of the source and can be ``x``, ``y``, or ``z``.
* ``f1 f2 f3`` are the coordinates (x,y,z) of the source in the model.
* ``f4 f5`` are optional parameters. ``f4`` is a time delay in starting the source. ``f5`` is a time to remove the source. If the time window is longer than the source removal time then the source will stop after the source removal time. If the source removal time is longer than the time window then the source will be active for the entire time window. If ``f4 f5`` are omitted the source will start at the beginning of time window and stop at the end of the time window.
* ``str1`` is the identifier of the waveform that should be used with the source.

For example, to use a x polarised Hertzian dipole with unit amplitude and a 600 MHz centre frequency Ricker waveform, use: ``#waveform: ricker 1 600e6 my_ricker_pulse`` and ``#hertzian_dipole: x 0.05 0.05 0.05 my_ricker_pulse``.

#magnetic_dipole:
-----------------

This will simulate an infinitesimal magnetic dipole. This is often referred to as an additive or soft source. The syntax of the command is:

.. code-block:: none

    #magnetic_dipole: c1 f1 f2 f3 [f4 f5] str1

* ``c1`` is the polarisation of the source and can be ``x``, ``y``, or ``z``.
* ``f1 f2 f3`` are the coordinates (x,y,z) of the source in the model.
* ``f4 f5`` are optional parameters. ``f4`` is a time delay in starting the source. ``f5`` is a time to remove the source. If the time window is longer than the source removal time then the source will stop after the source removal time. If the source removal time is longer than the time window then the source will be active for the entire time window. If ``f4 f5`` are omitted the source will start at the beginning of time window and stop at the end of the time window.
* ``str1`` is the identifier of the waveform that should be used with the source.

#voltage_source:
----------------

Allows you to introduce a voltage source at the position of an electric field component either as a hard source (i.e. replacing the value of electic field component) or, as having an internal lumped resistance. It is useful for exciting GPR antennas when the physical properties of the antenna are included in the model. The syntax of the command is:

.. code-block:: none

    #voltage_source: c1 f1 f2 f3 f4 [f5 f6] str1

* ``c1`` is the polarisation of the source and can be ``x``, ``y``, or ``z``.
* ``f1 f2 f3`` are the coordinates (x,y,z) of the source in the model.
* ``f4`` is the internal resistance of the voltage source in Ohms. If ``f4`` is set to zero then the voltage source is a hard source. That means it prescribes the value of the electric field component. If the waveform becomes zero then the source is perfectly reflecting.
* ``f5 f6`` are optional parameters. ``f5`` is a time delay in starting the source. ``f6`` is a time to remove the source. If the time window is longer than the source removal time then the source will stop after the source removal time. If the source removal time is longer than the time window then the source will be active for the entire time window. If ``f5 f6`` are omitted the source will start at the beginning of time window and stop at the end of the time window.
* ``str1`` is the identifier of the waveform that should be used with the source.

For example, to specify a y directed voltage source with an internal resistance of 50 Ohms, an amplitude of five, and a 1.2 GHz centre frequency Gaussian waveform use: ``#waveform: gaussian 5 1.2e9 my_gauss_pulse`` and ``#voltage_source: y 0.05 0.05 0.05 50 my_gauss_pulse``.

#rx:
----

Allows you to introduce output points into the model. These are locations where the values of the electric and magnetic field components over the number of iterations of the model will be saved to file. The syntax of the command is:

.. code-block:: none

    #rx: f1 f2 f3

``f1 f2 f3`` are the coordinates (x,y,z) of the receiver in the model.

#rx_box:
--------

Provides a simple method of defining multiple output points in the model. The syntax of the command is:

.. code-block:: none

    #rx_box: f1 f2 f3 f4 f5 f6 f7 f8 f9

* ``f1 f2 f3`` are the lower left (x,y,z) coordinates of the output volume, and ``f4 f5 f6`` are the upper right (x,y,z) coordinates of the output volume.
* ``f7 f8 f9`` are the increments (x,y,z) which define the number of output points in each direction. The minimum value of ``f7`` is :math:`\Delta x`, the minimum value of ``f8`` is :math:`\Delta y`, and the minimum value of ``f9`` is :math:`\Delta z`.

#src_steps: and #rx_steps:
--------------------------

Provide a simple method to allow you to move the location of all sources (``#src_steps``) or all receivers (``#rx_steps``) between runs of a model. The syntax of the commands is:

.. code-block:: none

    #src_steps: f1 f2 f3
    #rx_steps: f1 f2 f3

``f1 f2 f3`` are increments (x,y,z) to move all sources (``#hertzian_dipole``, ``#magnetic_dipole``, or ``#voltage_source``) or all receivers (created using either ``#rx`` or ``#rx_box`` commands).

.. _pml:

PML commands
============

The default behaviour is for gprMax to use a first order CFS PML that has a thickness of 10 cells on each of the six sides of the model domain. This can be altered by using the following commands.

#pml_cells:
------------

Allows you to control the number of cells of PML that are used on the six sides of the model domain. The PML is defined within the model domain, i.e. it is not added to the domain size. The syntax of the command is:

.. code-block:: none

    #pml_cells: i1 [i2 i3 i4 i5 i6]

* ``i1`` is the number of cells of PML to use on all sides of the model domain, or ``i1`` is the number of cells of PML to use on the side of the model domain in the negative x-axis direction.
* ``i2`` is the number of cells of PML to use on the side of the model domain in the negative y-axis direction.
* ``i3`` is the number of cells of PML to use on the side of the model domain in the negative z-axis direction.
* ``i4`` is the number of cells of PML to use on the side of the model domain in the positive x-axis direction.
* ``i5`` is the number of cells of PML to use on the side of the model domain in the positive y-axis direction.
* ``i6`` is the number of cells of PML to use on the side of the model domain in the positive z-axis direction.
* ``i1 i2 i3 i4 i5 i6`` may be set to zero to turn off the PML on a specific side of the model domain.

To create a 2D model (a one cell slice of 3D) switch off the PML in the one cell (infinite) direction, e.g. to create a 2D model in the x-y plane, with a dimension of one cell in the z direction, and 10 cells of PML elsewhere, use the command:

.. code-block:: none

    #pml_cells: 10 10 0 10 10 0

#pml_cfs:
---------

Allows you (advanced) control of the parameters that are used to build each order of the PML. Up to a second order PML can currently be specified, i.e. by using two ``#pml_cfs`` commands. The syntax of the command is:

.. code-block:: none

    #pml_cfs: str1 f1 f2 str2 f3 f4 str3 f5 f6

* ``str1`` is the type of scaling to use for the CFS :math:`\alpha` parameter. It can be ``constant``, ``linear``, ``inverselinear``, ``quadratic``, ``cubic``, and ``quartic``.
* ``f1 f2`` are the minimum and maximum values for the CFS :math:`\alpha` parameter.
* ``str2`` is the type of scaling to use for the CFS :math:`\kappa` parameter. It can be ``constant``, ``linear``, ``inverselinear``, ``quadratic``, ``cubic``, and ``quartic``.
* ``f3 f4`` are the minimum and maximum values for the CFS :math:`\kappa` parameter.
* ``str3`` is the type of scaling to use for the CFS :math:`\sigma` parameter. It can be ``constant``, ``linear``, ``inverselinear``, ``quadratic``, ``cubic``, and ``quartic``.
* ``f5 f6`` are the minimum and maximum values for the CFS :math:`\sigma` parameter.

The CFS values (which are internally specified) used for the default first order PML are: ``#pml_cfs: constant 0 0 constant 1 1 quartic 0 None``. Specifying 'None' for the maximum value of :math:`\sigma` forces gprMax to calculate it internally based on the relative permittivity and permeability of the underlying materials in the model.
