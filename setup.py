from distutils.core import setup

setup(name = 'cairis',
      version = '1.0',
      description='Computer Aided Integration of Requirements and Information Security',
      author = 'Shamal Faily',
      author_email = 'shamal.faily@googlemail.com',
      url = 'http://cairis.org',
      packages=['cairis'],
      package_data={'cairis':['cairis/*']}
     )
