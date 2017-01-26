try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Import Requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='SPECdata',
      version='1.0',
      description='Spectroscopic analysis tool',
      author='Jasmine Oliveira',
      author_email='jasmine.oliveira@cfa.harvard.edu',
      url='https://github.com/jnicoleoliveira/SPECData',
      install_requires=requirements
      )