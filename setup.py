#!/usr/bin/env python

import os
from setuptools import setup, find_packages

LONG_DESCRIPTION = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(name="Py-X",
      version="0.1",
      zip_safe=True,
      keywords="py-x unit test testing unittest unittesting xunit nunit junit xml",
      author="Per Fagrell",
      author_email="per.fagrell@gmail.com",
      license="PSF",
      package_data={'': ['data/*.xsd']},
      test_suite="nose.collector",
      tests_require=[
          "PyHamcrest",
          "mock",
          "lettuce"
      ],
      install_requires=[
          "lxml",
          "PyYaml"
      ],
      entry_points={
          'console_scripts': [
              'yaml2xunit = py_x:main'
          ]
        },
      classifiers=[
          'Development Status :: 1 - Pre-alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development'
          'Topic :: Software Development :: Testing'
        ],
      platforms=['All'],
      long_description=LONG_DESCRIPTION,
      packages=find_packages())


