from distutils.core import setup

setup(name = 'cairis',
      version = '1.0',
      description='Computer Aided Integration of Requirements and Information Security',
      author = 'Shamal Faily',
      author_email = 'shamal.faily@googlemail.com',
      url = 'http://www.cs.ox.ac.uk/cairis',
      packages=['src'],
      package_dir={'src': 'src'},
      package_data={'src':['sql/*.sql','config/*','images/*.png']}
     )
