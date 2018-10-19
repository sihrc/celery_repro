#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name='celery_race_condition',
    version='0.1',
    description='Reproducing race condition from celery redis backend',
    author='Chris Lee',
    author_email='chris@indico.io',
    packages=find_packages(),
    install_requires=open(
        os.path.join(
            os.path.dirname(__file__),
            "requirements.txt"
        ),
        'r'
    ).readlines()
)
