from setuptools import setup

setup(
  name='PyCorrelationMatrixManager',
  version='0.1.0',
  author='Chris Culver',
  packages=['PyCorrelationMatrixManager'],
  license='LICENSE.txt',
  description='Package for managing correlation matrices',
  long_description=open('README.md').read(),
  install_requires=open('requirements.py').read()
)
