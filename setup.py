from distutils.core import setup
setup(
  name = 'download_airnow_web',
  packages = ['download_airnow_web'], # this must be the same as the name above
  version = '1.01',
  description = 'Download data from airnow channel NOT using their API, but using the website.',
  author = 'Mike Smith',
  author_email = 'm.t.smith@sheffield.ac.uk',
  url = 'https://github.com/lionfish0/download_airnow_web.git',
  keywords = ['download','airnow','web'],
  classifiers = [],
  install_requires=['pandas'],
)

