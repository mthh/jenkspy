# -*- coding: utf-8 -*-
import numpy as np
from collections.abc import Iterable, Sequence
from typing import List, Dict, Union
from . import jenks


class JenksNaturalBreaks:
    """
    A class that can be used to classify a sequence of numbers into groups (clusters) using Fisher-Jenks natural breaks.
    """

    def __init__(self, n_classes: int = 6) -> None:
        """
        Parameters
        ----------
        n_classes : int
            The number of classes to be generated by the classifier.
        """
        self.n_classes = n_classes

    def __repr__(self) -> str:
        return f"JenksNaturalBreaks(n_classes={self.n_classes})"

    def __str__(self) -> str:
        return f"JenksNaturalBreaks(n_classes={self.n_classes})"

    def fit(self, x: Sequence[float]) -> None:
        """
        Parameters
        ----------
        x : array-like
            The sequence of numbers (integer/float) to be classified.

        """
        self.breaks_ = jenks_breaks(x, self.n_classes)
        self.inner_breaks_ = self.breaks_[1:-1]  # because inner_breaks is more
        self.labels_ = self.predict(x)
        self.groups_ = self.group(x)

    def predict(self, x: Union[float, Iterable[float]]) -> np.ndarray:
        """
        Predicts the class of each element in x.

        Parameters
        ----------
        x : array-like

        Returns
        -------
        list
        """
        if not isinstance(x, Iterable):
            return np.array(self.get_label_(x, idx=0))
        labels_ = []
        for val in x:
            label_ = self.get_label_(val, idx=0)
            labels_.append(label_)
        return np.array(labels_)

    def group(self, x: Sequence[float]) -> List[np.ndarray]:
        """
        Groups the elements in x into groups according to the classifier.

        Parameters
        ----------
        x : array-like
            The sequence of numbers (integer/float) to be classified.

        Returns
        -------
        list
            The list of groups that contains the values of x.
        """
        arr = np.array(x)
        groups_ = [arr[arr <= self.inner_breaks_[0]]]
        for idx in range(len(self.inner_breaks_))[:-1]:
            groups_.append(arr[(arr > self.inner_breaks_[idx])*(arr <= self.inner_breaks_[idx + 1])])
        groups_.append(arr[arr > self.inner_breaks_[-1]])
        return groups_

    def goodness_of_variance_fit(self, x: Sequence[float]) -> float:
        """
        Parameters
        ----------
        x : array-like

        Returns
        -------
        float
            The goodness of variance fit.
        """
        arr = np.array(x)
        array_mean = np.mean(arr)
        sdam = sum([(value - array_mean) ** 2 for value in arr])
        sdcm = 0
        for group in self.groups_:
            group_mean = np.mean(group)
            sdcm += sum([(value - group_mean) ** 2 for value in group])
        gvf = (sdam - sdcm)/sdam
        return gvf

    def get_label_(self, val: float, idx: int = 0) -> int:
        """
        Compute the group label of the given value.

        Parameters
        ----------
        val : float
            The value to be classified.
        idx : int, optional

        Returns
        -------
        int : The label of the value.
        """
        try:
            if val <= self.inner_breaks_[idx]:
                return idx
            else:
                idx = self.get_label_(val, idx + 1)
                return idx
        except:
            return len(self.inner_breaks_)


def validate_input(values: Sequence[float], n_classes: int) -> int:
    # Check input so that we have a sequence of numbers
    if not isinstance(values, Iterable) or isinstance(values, (str, bytes)):
        raise TypeError("A sequence of numbers is expected")

    # Number of classes have to be an integer
    if isinstance(n_classes, float) and int(n_classes) == n_classes:
        n_classes = int(n_classes)
    if not isinstance(n_classes, int):
        raise TypeError(
            "Number of class have to be a positive integer: "
            "expected an instance of 'int' but found {}"
            .format(type(n_classes)))

    # Check that numpy arrays are 1-dimensional
    if isinstance(values, np.ndarray):
        if len(values.shape) != 1:
            raise ValueError("A 1D array is expected")

    # Check that all values are finite (and can be cast safely to double later)
    try:
        if not np.isfinite(values).all():
            raise ValueError("All values have to be finite")
    except TypeError as e:
        import sys
        _, value, traceback = sys.exc_info()
        raise TypeError(
            "The sequence of values contains values that will overflow C double capacities - %s"
            .format(value)
        ).with_traceback(traceback)

    # Check that the number of classes is lesser than or equal to the length of unique values
    # and greater than or equal to 1
    if n_classes > len(np.unique(values)) or n_classes < 1:
        raise ValueError("Number of class have to be an integer greater than or equal to 1 and "
                         "smaller than or equal to the number of unique values to use")

    return n_classes


def jenks_breaks(values: Sequence[float], n_classes: int) -> List[float]:
    """
    Compute natural breaks (Fisher-Jenks algorithm) on a sequence of `values`,
    given `n_classes`, the number of desired class.

    Parameters
    ----------
    values : array-like
        The sequence of numbers (integer/float) to be used.
    n_classes : int
        The desired number of class. Have to be lesser than or equal
        to the length of `values` and greater than or equal to 1.

    Returns
    -------
    breaks : list of floats
        The computed break values, including minimum and maximum, in order
        to have all the bounds for building `n_classes` classes,
        so the returned list has a length of `n_classes` + 1.


    Examples
    --------
    Using n_classes = 3, expecting 4 break values , including min and max :

    >>> jenks_breaks(
            [1.3, 7.1, 7.3, 2.3, 3.9, 4.1, 7.8, 1.2, 4.3, 7.3, 5.0, 4.3],
            n_classes = 3)  # Should output [1.2, 2.3, 5.0, 7.8]

    """
    n_classes = validate_input(values, n_classes)
    return jenks._jenks_breaks(values, n_classes)


def _jenks_matrices(values: Sequence[float], n_classes: int, testing_algo: bool = False) -> Dict[str, np.ndarray]:
    """
    Returns the intermediate matrices (lower_class_limits and variance combinations)
    that are created when computing natural breaks (Fisher-Jenks algorithm) on a sequence of `values`,
    given `n_classes`, the number of desired class.
    This is only used for testing and debugging purpose, it is not part of the supported API
    and might disappear at any time.

    Parameters
    ----------
    values : array-like
        The sequence of numbers (integer/float) to be used.
    n_classes : int
        The desired number of class. Have to be lesser than or equal
        to the length of `values` and greater than or equal to 1.
    testing_algo : bool
        If False, use the 'normal' version of the algorithm to compute the
        matrices, if True, use the version of the algorithm that mimic
        Fortran implementation by using the same indexing.

    Returns
    -------
    dict : The computed matrices, as numpy arrays,
           in a dict with keys 'lower_class_limits' and 'variance_combinations'.
    """
    n_classes = validate_input(values, n_classes)

    if testing_algo not in (True, False):
        raise ValueError('testing_algo parameters have to be either True or False')

    return jenks._jenks_matrices(values, n_classes, testing_algo)
