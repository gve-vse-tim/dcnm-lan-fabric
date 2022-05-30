#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dcnm-lan-fabric",
    version="0.2.2",
    author="Tim Miller",
    author_email="timmil@cisco.com",
    description="Python interface to handle Cisco DCNM/NDFC API communication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gve-vse-tim/dcnm-lan-fabric",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free To Use But Restricted",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'requests~=2.25.0',
        'click~=8.0.1',
        'typer~=0.4.1',
    ],
    scripts=[
        'bin/dcnmctl.py',
        'bin/ndfcctl.py',
    ]
)
