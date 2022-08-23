# -*- coding: utf-8 -*-
from distutils.core import setup
from distutils.extension import Extension
from ast import parse
from os import path

try:
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

ext = '.pyx' if USE_CYTHON else '.c'

exts = [
    Extension(
        "jenkspy.jenks",
        ["jenkspy/src/jenks" + ext],
        ["jenkspy"],
    )
]

with open(path.join('jenkspy', '__init__.py')) as f:
    __version__ = parse(next(filter(lambda line: line.startswith('__version__'),
                                     f))).body[0].value.s

with open('README.rst') as f:
    long_desc = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='jenkspy',
    version=__version__,
    license="MIT",
    ext_modules=cythonize(exts) if USE_CYTHON else exts,
    cmdclass={'build_ext': build_ext} if USE_CYTHON else {},
    packages=["jenkspy"],
    include_package_data=True,
    description="Compute Natural Breaks (Fisher-Jenks algorithm)",
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    install_requires=requirements,
    test_suite="tests",
    author="Matthieu Viry",
    author_email="matthieu.viry@cnrs.fr",
    url='http://github.com/mthh/jenkspy',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],
)
