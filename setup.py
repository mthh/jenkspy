# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import Extension

from Cython.Build import cythonize
from Cython.Distutils import build_ext

exts = [
    Extension(
        "jenkspy.jenks",
        ["jenkspy/src/jenks.pyx"],
        ["jenkspy"],
    )
]

setup(
    ext_modules=cythonize(exts),
    cmdclass={'build_ext': build_ext}
)
