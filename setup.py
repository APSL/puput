import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='puput',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    keywords="django wagtail puput blog cms app",
    description='A Django blog app implemented in Wagtail.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    install_requires=[
        'Django>=1.7.1,<1.9',
        'wagtail>=1.0',
        'django-endless-pagination==2.0',
        'tapioca-disqus==0.1.1',
    ],
    url='http://www.apsl.net/',
    author='Marc Tuduri',
    author_email='marctc@gmail.com',
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
