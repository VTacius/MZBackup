from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name='MZBackup',
    version='0.9.5',
    description='Migración/Backup de Usuarios y Cuentas en Zimbra',

    author='Alexander Ortíz',
    author_email='vtacius@gmail.com',

    license='GPLv3',
    keywords='backup python rust',

    packages=["mzbackup"],
    rust_extensions=[RustExtension("mzbackup.mzbackup", binding=Binding.PyO3)],
    # rust extensions are not zip safe, just like C-extensions.
    zip_safe=False,

    install_requires=[],

    test_suite="pytest",

    entry_points={
        'console_scripts': ['mzbackup=mzbackup.cli:main']
    },
)
