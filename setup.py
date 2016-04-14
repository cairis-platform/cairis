#!/usr/bin/env python

import os
from setuptools import setup

from distutils.core import setup
setup(name='cairis',
      version='1.0',
      author='Shamal Faily',
      author_email='shamal.faily@gmail.com',
      description = 'A security design tool',
      license = 'Apache Software License',
      url='http://cairis.org',
      packages=['core','gui','mio'],
      scripts=['cairis.py','cimport.py','cexport.py'],
      data_files=[('config',['config/*.dtd','config/cairis.cnf']),
                  ('images',['images/*.png'])],
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
      )

