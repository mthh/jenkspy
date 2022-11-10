Changes
=======

0.3.2 (2022-11-10)
------------------

- Add type hints and fix some docstring about parameters and return types, thanks to Kim Hyeonseok / @plming (#27).

0.3.1 (2022-08-23)
------------------

- Add missing requirements.txt file in MANIFEST.in and in sdist package.

0.3.0 (2022-08-23)
------------------

- Add NumPy as a mandatory dependency.

- Only compute matrices in C code and move sorting the values, casting to double, and computing the actual breaks to Python/Cython code for better maintainability.

- Improve performance by using 1D arrays instead of 2D arrays in ``JenksBreakValues`` C function.

- Preserve the precision of the original list/array of values in the returned breaks.

- Fix bug when requesting a number of class equal to the number of values.

- Raise an exception when the number of classes is greater than the number of unique values (however this might change in the future by choosing to return a list of breaks shorter than the one requested by the user).

- Rename ``nb_class`` parameter to ``n_classes`` (notably to be closer to sklearn ``n_clusters`` parameter).


0.2.4 (2022-08-18)
------------------

- Update package metadata and docstrings.


0.2.3 (2022-08-18)
------------------

- Check size of integer values given to ``jenks_breaks`` function to avoid Segfault when casting to C double (fixes #23).

- Raise an error (instead of printing a warning) when target array contains non-finite values (fixes #23).

- Raise an error when the target numpy.ndarray is not one-dimensional (fixes #25).

- Improve implementation of ``JenksBreakValues`` C function by using better variable naming and by simplifying the construction of the 'breaks' array (should partly fix #22).

- Add docstrings to ``JenksNaturalBreaks`` methods.


0.2.2 (2022-08-12)
------------------

- Update docstring to fix return type of ``jenks_breaks`` (fix #26).


0.2.1 (2022-08-12)
------------------

- Add a method to the ``JenksNaturalBreaks`` class that calculates the Goodness of Fit Variance thanks to Maurício Gomes / @mgomesq (#17).

- Add optional download numpy using ``[interface]`` thanks to Muhammad Yasirroni / @yasirroni (#16).

- Replace Travis / AppVeyor by GitHub Actions to build wheels for currently supported python versions on Windows / MacOs / Linux (according to https://devguide.python.org/versions/#supported-versions)


0.2.0 (2020-10-18)
------------------

- Add ``JenksNaturalBreaks`` for computing breaks in a more object-oriented manner, with an interface similar to those provided by scikit-learn *(requires Numpy to take full advantage of it)* (thanks to @yasirroni, #11)


0.1.6 (2020-09-02)
------------------

- Removes support for Python2 (simplifies some minor parts of the code) and add Python 3.8 to the appveyor matrix.

- Updates docstrings and README to clarify that the result includes the lower and upper value.


0.1.5 (2018-11-15)
------------------

- Fix segfault occurring when the input array was containing NaN or Inf values (#4).

- Create this changelog.

