#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='precision_metagenomics_pipeline',
    version='0.1.0',
    description="Cohesive pipelines for precision metagenomics",
    long_description=readme + '\n\n' + history,
    author="David C Danko",
    author_email='dcd3001@med.cornell.edu',
    url='https://github.com/dcdanko/precision_metagenomics_pipeline',
    packages=[
        'precision_metagenomics_pipeline',
    ],
    package_dir={'precision_metagenomics_pipeline':
                 'precision_metagenomics_pipeline'},
    entry_points={
        'console_scripts': [
            'precision_metagenomics_pipeline=precision_metagenomics_pipeline.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='precision_metagenomics_pipeline',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
