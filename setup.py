#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()


with open('HISTORY.rst') as history_file:
    history = history_file.read()


requirements = [
    'Click>=6.0',
    'tinydb',
    'snakemake',
]


test_requirements = [
    # TODO: put package test requirements here
]


setup(
    name='meta_ultra',
    version='0.1.0',
    description='Cohesive pipelines for precision metagenomics',
    long_description=readme + '\n\n' + history,
    author='David C Danko',
    author_email='dcd3001@med.cornell.edu',
    url='https://github.com/dcdanko/meta_ultra',
    packages=find_packages(exclude=['tests', 'scripts']),
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords='meta_ultra',
    entry_points={
        'console_scripts': [
            'mu=meta_ultra.cli:main'
        ]
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
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
    tests_require=test_requirements,
)
