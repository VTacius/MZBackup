from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name='remoto',
    version='0.9.45',
    description='Backup de indices en Elasticsearch 6.x',
    keywords='backup python rust',
    author='Alexander Ortíz',
    author_email='vtacius@gmail.com',
    license='GPLv3',

    packages=["remoto"],
    rust_extensions=[RustExtension("remoto.remoto", binding=Binding.PyO3)],
    # rust extensions are not zip safe, just like C-extensions.
    zip_safe=False,

    install_requires=[],

    test_suite="pytest",

    entry_points = {
        'console_scripts': ['remoto=remoto.cli:main']
        },

)

