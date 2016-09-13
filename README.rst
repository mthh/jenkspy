Fast Jenks breaks for Python
============================

Compute "natural" break values (Jenks algorythm) on list/tuple/numpy.ndarray of integers/floats.

(Intented compatibility: CPython 2.7+ and 3.3+)

|Build Status travis| |Build status appveyor|

Usage :
-------

.. code:: python

    >>> import random
    >>> list_of_values = [random.random()*5000 for _ in range(12000)]

    >>> import jenkspy
    >>> breaks = jenkspy.jenks_breaks(list_of_values, nb_class=6)

    >>> import json
    >>> with open('test.json', 'r') as f:
    ...     data = json.loads(f.read())
    ...
    >>> jenkspy.jenks_breaks(data, nb_class=5)
    (0.0028109620325267315, 2.0935479691252112, 4.205495140049607, 6.178148351609707, 8.09175917180255, 9.997982932254672)

Installation :
--------------

.. code:: shell

    pip install jenkspy

.. code:: shell

    git clone http://github.com/mthh/jenkspy
    cd jenkspy/
    python setup.py install

Requirements (only for building from source):
----------------------------------------------

-  C compiler
-  Python C headers

Motivation :
------------

-  Could be used as an eventual dependency in other package (using
   *appveyor* and *travis* to build wheels for easier installation via
   ``pip``).
-  Getting the break values! (and fast!)
-  Other python implementations are currently existing.

.. |Build Status travis| image:: https://travis-ci.org/mthh/jenkspy.svg?branch=master
   :target: https://travis-ci.org/mthh/jenkspy

.. |Build status appveyor| image:: https://ci.appveyor.com/api/projects/status/9ffk6juf2499xqk0/branch/master?svg=true
   :target: https://ci.appveyor.com/project/mthh/jenkspy/branch/master
