import os
import subprocess

from setuptools import setup

from setuptools.command.install_lib import install_lib as _install_lib
from setuptools.command.develop import develop as _develop
from distutils.command.build import build as _build
from distutils.cmd import Command


class compileTranslations(Command):
    description = 'compile message catalogs to MO files via pybabel command'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("\nCompiling translations:")
        subprocess.call( os.path.join(os.path.dirname(__file__), "webant/babel/trans_compile.sh") )

class build(_build):
    sub_commands = [('compileTranslations', None)] + _build.sub_commands


class install_lib(_install_lib):
    def run(self):
        self.run_command('compileTranslations')
        _install_lib.run(self)

class develop(_develop):
     def run(self):
        self.run_command('compileTranslations')
        _develop.run(self)

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as buf:
        return buf.read()

setup(name='libreant',
      version='0.1',
      description='{e,}book archive focused on small grass root archives, distributed search, low assumptions',
      long_description=read('README.mdwn'),
      author='insomnialab',
      author_email='insomnialab@hacari.org',
      url='https://github.com/insomnia-lab/libreant',
      license='AGPL',
      packages=['libreantdb', 'webant', 'webant.presets'],
      install_requires=[
          'gevent',
          'elasticsearch',
          'flask-bootstrap',
          'Flask-Babel',
          'flask-appconfig',
          'Flask',
          'opensearch',
          'Fsdb'
      ],
      include_package_data=True,
      tests_require=['nose'],
      test_suite='nose.collector',
      zip_safe=False,
      cmdclass={'build': build,
                'install_lib': install_lib,
                'develop':develop,
                'compileTranslations': compileTranslations },
      entry_points={'console_scripts': [
          'webant=webant.webant:main',
          'agherant=webant.agherant_standalone:main'
      ] },
      classifiers=[
                  "Framework :: Flask",
                  "License :: OSI Approved :: GNU Affero General Public License v3",
                  "Operating System :: POSIX :: Linux",
                  "Programming Language :: Python :: 2"
                  "Development Status :: 4 - Beta"
                  ]
      )
