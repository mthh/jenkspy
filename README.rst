Fast Fisher-Jenks breaks for Python
===================================

Compute "natural breaks" (*Fisher-Jenks algorithm*) on list / tuple / array / numpy.ndarray of integers/floats.

The algorithm implemented by this library is also sometimes referred to as *Fisher-Jenks algorithm*, *Jenks Optimisation Method* or *Fisher exact optimization method*. This is a deterministic method to calculate the optimal class boundaries.

Intended compatibility: CPython 3.6+

Wheels are provided via PyPI for Windows / MacOS / Linux users - Also available on conda-forge channel for Anaconda users.

|Version| |Anaconda-Server Badge| |Build Status GH| |PyPI download month|

Usage
-----

Two ways of using `jenkspy` are available:

- by using the ``jenks_breaks`` function which takes as input a `list <https://docs.python.org/3/library/stdtypes.html#list>`_ / `tuple <https://docs.python.org/3/library/stdtypes.html#tuple>`_ / `array.array <https://docs.python.org/3/library/array.html#array.array>`_ / `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ of integers or floats and returns a list of values that correspond to the limits of the classes (starting with the minimum value of the series - the lower bound of the first class - and ending with its maximum value - the upper bound of the last class).

.. code:: python

    >>> import jenkspy
    >>> import json

    >>> with open('tests/test.json', 'r') as f:
    ...     # Read some data from a JSON file
    ...     data = json.loads(f.read())
    ...
    >>> jenkspy.jenks_breaks(data, n_classes=5) # Asking for 5 classes
    [0.0028109620325267315, 2.0935479691252112, 4.205495140049607, 6.178148351609707, 8.09175917180255, 9.997982932254672]
    # ^                      ^                    ^                 ^                  ^                 ^
    # Lower bound            Upper bound          Upper bound       Upper bound        Upper bound       Upper bound
    # 1st class              1st class            2nd class         3rd class          4th class         5th class
    # (Minimum value)                                                                                    (Maximum value)


- by using the ``JenksNaturalBreaks`` class that is inspired by ``scikit-learn`` classes.

The ``.fit`` and ``.group`` behavior is slightly different from ``jenks_breaks``, by accepting value outside the range of the minimum and maximum value of ``breaks_``, retaining the input size. It means that fit and group will use only the ``inner_breaks_``. All value below the min bound will be included in the first group and all value higher than the max bound will be included in the last group.

.. code:: python

    >>> from jenkspy import JenksNaturalBreaks

    >>> x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    >>> jnb = JenksNaturalBreaks(4) # Asking for 4 clusters

    >>> jnb.fit(x) # Create the clusters according to values in 'x'
    >>> print(jnb.labels_) # Labels for fitted data
    ... print(jnb.groups_) # Content of each group
    ... print(jnb.breaks_) # Break values (including min and max)
    ... print(jnb.inner_breaks_) # Inner breaks (ie breaks_[1:-1])
    [0 0 0 1 1 1 2 2 2 3 3 3]
    [array([0, 1, 2]), array([3, 4, 5]), array([6, 7, 8]), array([ 9, 10, 11])]
    [0.0, 2.0, 5.0, 8.0, 11.0]
    [2.0, 5.0, 8.0]

    >>> print(jnb.predict(15)) # Predict the group of a value
    3

    >>> print(jnb.predict([2.5, 3.5, 6.5])) # Predict the group of several values
    [1 1 2]

    >>> print(jnb.group([2.5, 3.5, 6.5])) # Group the elements into there groups
    [array([], dtype=float64), array([2.5, 3.5]), array([6.5]), array([], dtype=float64)]


Installation
------------

+ **From pypi**

.. code:: shell

    pip install jenkspy


+ **From source**

.. code:: shell

    git clone http://github.com/mthh/jenkspy
    cd jenkspy/
    python setup.py install

+ **For anaconda users**

.. code:: shell

    conda install -c conda-forge jenkspy


Requirements :
--------------

- `Numpy <https://numpy.org>`_

-  Only for building from source: C compiler, Python C headers, setuptools and Cython.


Motivation :
------------

-  Making a painless installing C extension so it could be used more easily
   as a dependency in an other package (and so learning how to build wheels
   using *appveyor* / *travis* at first - now it uses *GitHub Actions*).
-  Getting the break values! (and fast!). No fancy functionality provided,
   but contributions/forks/etc are welcome.
-  Other python implementations are currently existing but not as fast or not available on PyPi.

.. |Build status GH| image:: https://github.com/mthh/jenkspy/actions/workflows/wheel.yml/badge.svg
   :target: https://github.com/mthh/jenkspy/actions/workflows/wheel.yml

.. |Version| image:: https://img.shields.io/pypi/v/jenkspy.svg?color=007ec6
   :target: https://pypi.python.org/pypi/jenkspy

.. |Anaconda-Server Badge| image:: https://anaconda.org/conda-forge/jenkspy/badges/version.svg
   :target: https://anaconda.org/conda-forge/jenkspy

.. |PyPI download month| image:: https://img.shields.io/pypi/dm/jenkspy.svg
   :target: https://pypi.python.org/pypi/jenkspy
