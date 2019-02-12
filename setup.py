# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='charlesxlogminmax',
    version='0.0.1',
    description='Extract and plot the min and max info of CharlesX log',
    long_description=readme,
    author='Quentin Douasbin',
    author_email='douasbin@stanford.edu',
    url='https://github.com/?',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

