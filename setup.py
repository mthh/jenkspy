# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    USE_CYTHON = True
except:
    USE_CYTHON = False

ext = '.pyx' if USE_CYTHON else '.c'

exts = [Extension("jenkspy.jenks",
            ["jenkspy/src/jenks" + ext], ["jenkspy"])]

setup(
    name='jenkspy',
    version='0.1.0',
    license="MIT",
    ext_modules=cythonize(exts) if USE_CYTHON else exts,
    cmdclass = {'build_ext': build_ext} if USE_CYTHON else {},
    packages=find_packages(),
    description="Compute Natural Breaks (Jenks algorythm)",
    test_suite="test_jenks",
    author="mthh",
    url='http://github.com/mthh/jenkspy',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Scientific/Engineering",
        ],
    )
