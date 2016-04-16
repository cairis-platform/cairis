#!/usr/bin/env python

import os
from setuptools import find_packages,setup

EXCLUDE_FROM_PACKAGES = ['examples','scripts','test']

setup(name='cairis',
      version='1.0',
      author='Shamal Faily',
      author_email='shamal.faily@gmail.com',
      description = 'A security design tool',
      license = 'Apache Software License',
      url='http://cairis.org',
      packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
      include_package_data=True,
      scripts=['cairis/bin/cairis.py','cairis/bin/cimport.py','cairis/bin/cexport.py'],
      entry_points={'console_scripts': [
                       'cairis = cairis.bin.cairis:main']},
      classifiers=[
       "Development Status :: 4 - Beta",
       "Environment :: Console",
       "Environment :: X11 Applications :: Gnome",
       "Intended Audience :: Developers",
       "Intended Audience :: Education",
       "Intended Audience :: End Users/Desktop",
       "Intended Audience :: Information Technology",
       "Intended Audience :: Science/Research",
       "License :: OSI Approved :: Apache Software License",
       "Natural Language :: English",
       "Operating System :: POSIX :: Linux",
       "Programming Language :: PL/SQL",
       "Programming Language :: Python :: 2",
       "Programming Language :: SQL",
       "Topic :: Office/Business",
       "Topic :: Security",
       ],
       install_requires = ['setuptools'],
      )

