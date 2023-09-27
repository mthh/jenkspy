# -*- coding: utf-8 -*-
from distutils.core import setup
from distutils.extension import Extension
from ast import parse
from os import path

from Cython.Distutils import build_ext
from Cython.Build import cythonize

ext = '.pyx'

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
    ext_modules=cythonize(exts),
    cmdclass={'build_ext': build_ext},
    packages=["jenkspy"],
    include_package_data=True,
    description="Compute Natural Breaks (Fisher-Jenks algorithm)",
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    install_requires=requirements,
    test_suite="tests",
    author="Matthieu Viry",
    author_email="matthieu.viry@cnrs.fr",
    url='https://github.com/mthh/jenkspy',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Typing :: Typed",
    ],
)
