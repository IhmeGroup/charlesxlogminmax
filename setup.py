# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("./requirements.txt")

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

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
    install_reqs = reqs,
    packages=find_packages(exclude=('test', 'docs'))
)

