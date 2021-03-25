
from setuptools import setup

setup(name='Python Spiders',
      version='0.1',
      description='A bunch of python crawlers',
      url='http://github.com/icarus612/daedalus-crawlers-PY',
      author='Icarus612',
      author_email='ellishogan95@gmail.com',
      license='MIT',
      install_requires=[
          'requests',
          'bs4',
					'argparse',
					're',
					'os',
					'json'
      ],
      zip_safe=False)