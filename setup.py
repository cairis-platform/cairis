#!/usr/bin/env python

import os
from setuptools import setup

setup(name='cairis',
      version='0.4',
      author='Shamal Faily',
      author_email='shamal.faily@gmail.com',
      description = 'A security design tool',
      license = 'Apache Software License',
      url='https://github.com/failys/cairis',
      download_url='https://github.com/failys/cairis/tarball/0.4',
      packages=['cairis'],
      data_files = [ ('share/examples', [examples]) ],
      include_package_data=True,
      scripts=['cairis/bin/cairis_gui.py','cairis/bin/cimport.py','cairis/bin/cexport.py','cairis/bin/at2om.py','cairis/bin/gt2pc.py'],
      entry_points={'console_scripts': [
                       'cairis_gui = cairis.bin.cairis_gui:main',
                       'cimport = cairis.bin.cimport:main',
                       'cexport = cairis.bin.cexport:main',
                       'at2om = cairis.bin.at2om:main',
                       'gt2pc = cairis.bin.gt2pc:main']},
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
      install_requires = [
       "setuptools",
       "mysql-python",
       "pyparsing",
       "pydot"
      ],
      setup_requires = ['pytest-runner'],
      test_requires = ['pytest']
     )

