# -*- coding: utf-8 -*-

import os
import io
import re

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def read(*parts):
    with io.open(os.path.join(os.path.dirname(__file__), *parts)) as f:
        return f.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = read(os.path.join(package, '__init__.py'))
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


def get_author(package):
    """
    Return package author as listed in `__author__` in `init.py`.
    """
    init_py = read(os.path.join(package, '__init__.py'))
    return re.search("^__author__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


def get_email(package):
    """
    Return package email as listed in `__email__` in `init.py`.
    """
    init_py = read(os.path.join(package, '__init__.py'))
    return re.search("^__email__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)

setup(
    name='puput',
    version=get_version('puput'),
    packages=find_packages(),
    include_package_data=True,
    keywords="django wagtail puput blog cms app",
    description='A Django blog app implemented in Wagtail.',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    install_requires=[
        'Django>=1.7.1,<1.9',
        'wagtail>=1.0,<2.0',
        'django-endless-pagination==2.0',
        'tapioca-disqus==0.1.1',
    ],
    url='http://github.com/APSL/puput',
    author=get_author('puput'),
    author_email=get_email('puput'),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ]
)
