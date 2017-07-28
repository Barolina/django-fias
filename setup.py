#!/usr/bin/env python
from setuptools import setup, find_packages
import codecs
import sys

from fias.version import __version__

sys.path.insert(0, '..')
PY3 = sys.version_info[0] == 3

extra_requirements = []
if PY3:
    extra_requirements = [
        'suds-jurko>=0.6',
    ]
else:
    extra_requirements = [
        'suds>=0.4',
    ]

setup(
    name='django-fias',
    version=__version__,
    author='Larisa',
    author_email='root@proscript.ru',
    url='https://github.com/Barolina/django-fias',
    download_url='https://github.com/Barolina/django-fias/archive/{0}.tar.gz'.format(__version__),

    description='FIAS Django integration',
    long_description=codecs.open('README.rst', encoding='utf8').read(),

    license='MIT license',
    install_requires=[
        'django>=1.7',
        'django_select2>=5.3.0',
        'rarfile',
        'six',
        'lxml',
        'unrar',
        'dbfread>=2.0.0',
    ] + extra_requirements,
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
