#!/usr/bin/env python3
from setuptools import setup

setup(
    name='pcsptools',
    version='0.0.2',
    description='Test whether polymorphisms satisfy some minor\
        identitites.',
    author='Jakub Opršal',
    author_email='oprsal.jakub@gmail.com',
    packages=["pcsptools"],
    install_requires=[
        "pycosat",
        ],
    package_dir={'': 'src'}
    )
