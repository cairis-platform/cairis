from distutils.core import setup

setup(name = 'cairis',
      version = '1.0',
      description='Computer Aided Integration of Requirements and Information Security',
      author = 'Shamal Faily',
      author_email = 'shamal.faily@googlemail.com',
      url = 'http://www.cs.ox.ac.uk/cairis',
      packages=['cairis'],
      package_dir={'src': 'cairis'},
      package_data={'cairis':['sql/*.sql','config/*.dtd','config/*.xml','config/*.pdf','config/*.png','config/*.xml','images/*.png']}
     )
