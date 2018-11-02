#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install


version = {}
with open('meta_ultra/version.py') as version_file:
    exec(version_file.read(), version)


with open('README.rst') as readme_file:
    readme = readme_file.read()


with open('HISTORY.rst') as history_file:
    history = history_file.read()


requirements = [
    'Click>=6.0',
    'tinydb==3.11.1',
    'snakemake==5.3.0',
    'py_archy==1.0.2',
    'metagenscope_api==0.1.0',
]

dependency_links = [
    'git+https://github.com/dcdanko/MetaGenScopeAPI.git#egg=metagenscope_api-0.1.0',
]


test_requirements = [
    # TODO: put package test requirements here
]


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version."""

    description = 'Verify that the git tag matches our version.'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != 'v{0}'.format(__version__):
            info = 'Git tag: {0} does not match the version of this app: {1}'
            info = info.format(tag, __version__)
            sys.exit(info)


setup(
    name='meta_ultra',
    version=version['__version__'],
    description='Cohesive pipelines for precision metagenomics',
    long_description=readme + '\n\n' + history,
    author=version['__author__'],
    author_email=version['__email__'],
    url='https://github.com/dcdanko/MetaUltra',
    packages=find_packages(exclude=['tests', 'scripts']),
    include_package_data=True,
    install_requires=requirements,
    dependency_links=dependency_links,
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
    cmdclass={
        'verify': VerifyVersionCommand,
    },
)
