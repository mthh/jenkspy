# -*- coding: utf-8 -*-
from collections import Iterable
from . import jenks


def jenks_breaks(values, nb_class):
    """
    Compute jenks natural breaks on a sequence of `values`, given `nb_class`,
    the number of desired class.

    Parameters
    ----------
    values : array-like
        The Iterable sequence of numbers (integer/float) to be used.
    nb_class : int
        The desired number of class (as some other functions requests
        a `k` value, `nb_class` is like `k` + 1). Have to be lesser than
        the length of `values` and greater than 2.

    Returns
    -------
    breaks : tuple of floats
        The computed break values, including minimum and maximum, in order
        to have all the bounds for building `nb_class` class,
        so the returned tuple has a length of `nb_class` + 1.


    Examples
    --------
    Using nb_class = 3, expecting 4 break values , including min and max :

    >>> jenks_breaks(
            [1.3, 7.1, 7.3, 2.3, 3.9, 4.1, 7.8, 1.2, 4.3, 7.3, 5.0, 4.3],
            nb_class = 3)  # Should output (1.2, 2.3, 5.0, 7.8)

    """

    if not isinstance(values, Iterable) or isinstance(values, (str, bytes)):
        raise TypeError("A sequence of numbers is expected")
    if isinstance(nb_class, float) and int(nb_class) == nb_class:
        nb_class = int(nb_class)
    if not isinstance(nb_class, int):
        raise TypeError(
            "Number of class have to be a positive integer: "
            "expected an instance of 'int' but found {}"
            .format(type(nb_class)))
    if nb_class >= len(values) or nb_class < 2:
        raise ValueError("Number of class have to be an integer "
                         "greater than 2 and "
                         "smaller than the number of values to use")
    return jenks._jenks_breaks(values, nb_class)
