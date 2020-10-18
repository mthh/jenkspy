Changes
=======



0.2.0 (2020-10-18)
------------------

- Add `JenksNaturalBreaks` for computing breaks in a more object-oriented manner, with an interface similar to those provided by scikit-learn *(requires Numpy to take full advantage of it)* (thanks to @yasirroni, #11)


0.1.6 (2020-09-02)
------------------

- Removes support for Python2 (simplifies some minor parts of the code) and add Python 3.8 to the appveyor matrix.

- Updates docstrings and README to clarify that the result includes the lower and upper value.


0.1.5 (2018-11-15)
------------------

- Fix segfault occurring when the input array was containing NaN or Inf values (#4).

- Create this changelog.

