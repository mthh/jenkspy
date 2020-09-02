# -*- coding: utf-8 -*-
import setuptools
from distutils.core import setup
from distutils.extension import Extension
from ast import parse
from os import path
try:
    from future_builtins import filter
except ImportError:
    pass

try:
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    USE_CYTHON = True
except:
    USE_CYTHON = False

ext = '.pyx' if USE_CYTHON else '.c'

exts = [Extension("jenkspy.jenks",
        ["jenkspy/src/jenks" + ext], ["jenkspy"])]

with open(path.join('jenkspy', '__init__.py')) as f:
    __version__ = parse(next(filter(lambda line: line.startswith('__version__'),
                                     f))).body[0].value.s

with open('README.rst') as f:
    long_desc = f.read()

setup(
    name='jenkspy',
    version=__version__,
    license="MIT",
    ext_modules=cythonize(exts) if USE_CYTHON else exts,
    cmdclass={'build_ext': build_ext} if USE_CYTHON else {},
    packages=["jenkspy"],
    include_package_data=True,
    description="Compute Natural Breaks (Jenks algorythm)",
    long_description=long_desc,
    test_suite="tests",
    author="Matthieu Viry",
    author_email="matthieu.viry@cnrs.fr",
    url='http://github.com/mthh/jenkspy',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        ],
    )
