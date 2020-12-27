#!/usr/bin/env python

import os
import fnmatch
from setuptools import setup

egFiles = []
for root, dirnames, fileNames in os.walk('examples'):
  for fileName in fnmatch.filter(fileNames,'*'):
    egFiles.append(os.path.join(root,fileName))


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='cairis',
      version='2.3.8',
      author='Shamal Faily',
      author_email='admin@cairis.org',
      description = 'A security design tool',
      license = 'Apache Software License',
      url='https://github.com/cairis-platform/cairis',
      download_url='https://github.com/cairis-platform/cairis/tarball/2.3.8',
      packages=['cairis'],
      include_package_data=True,
      data_files = [('cairis/examples', egFiles)],
      scripts=['cairis/bin/cairis_gui.py','cairis/bin/cairisd.py','cairis/bin/configure_cairis_db.py','cairis/bin/cimport.py','cairis/bin/cexport.py','cairis/bin/at2om.py','cairis/bin/gt2pc.py','cairis/bin/xr2cr.py'],
      entry_points={'console_scripts': [
                       'cairis_gui = cairis.bin.cairis_gui:main',
                       'configure_cairis_db = cairis.bin.configure_cairis_db:main',
                       'cimport = cairis.bin.cimport:main',
                       'cexport = cairis.bin.cexport:main',
                       'at2om = cairis.bin.at2om:main',
                       'gt2pc = cairis.bin.gt2pc:main',
                       'xr2cr = cairis.bin.xr2cr:main',
                       'add_cairis_user = cairis.bin.add_cairis_user:main']},
      classifiers=[
       "Development Status :: 5 - Production/Stable",
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
       "Programming Language :: Python :: 3",
       "Programming Language :: SQL",
       "Topic :: Office/Business",
       "Topic :: Security",
       ],
      install_requires = required,
      setup_requires = ['pytest-runner'],
      test_requires = ['pytest']
     )

