#!/usr/bin/env python3
from setuptools import setup


setup(
    name='pcsptools',
    version='0.0.5-alpha-3',
    description='Tools for checking identities in polymorphism minions.',
    author='Jakub Opršal',
    author_email='oprsal.jakub@gmail.com',
    license='MIT',
    packages=['pcsptools'],
    install_requires=['pycosat']
)
