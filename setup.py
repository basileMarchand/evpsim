#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib as pl
from setuptools import setup, find_packages
from evpsim import version
__author__ = 'Basile Marchand'

__version__ = version

name = 'evpsim'
contact = "basile.marchand@gmail.com"


here = pl.Path(__file__).parent.absolute()

requirements = []
with open(here / pl.Path("requirements.txt")) as fid:
    content = fid.read().split("\n")
    for line in content:
        if line.startswith("#") or line.startswith(" ") or line == "":
            continue
        elif line.startswith("-e"):
            pname = line.split("#egg=")[1]
            req_line = "{} @ {}".format(pname, line[3:])
            requirements.append(req_line)
        else:
            requirements.append(line)

with open(here / pl.Path("README.md")) as fid:
    long_description = fid.read()

extras_require = {'test': ['pytest', ]}


setup(
    name=name,
    version=__version__,
    author_email=contact,
    description="Python ElastoViscoPlastic mechanical behavior simulator",
    long_description=long_description,
    license="",
    url="",
    classifiers=[
        'Development Status :: 1 - Beta',
    ],
    install_requires=requirements,
    extras_require=extras_require,
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.svg"]},
    entry_points={
        'console_scripts': ['rcmat=rcmat.gui:main'],
    }
)
