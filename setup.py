from distutils.core import setup
setup(
  name = 'eremetic-synchronous-client',
  py_modules=['eremetic_synchronous_client'],
  version = '0.28.1',
  description = 'A synchronous client for Eremetic',
  author = 'Stefano Baghino',
  author_email = 'stefano@baghino.me',
  url = 'https://github.com/stefanobaghino/eremetic-synchronous-client',
  keywords = ['eremetic', 'mesos'],
  install_requires=['requests>=2.8.13'],
  classifiers = [],
)
