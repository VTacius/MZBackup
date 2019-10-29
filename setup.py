# coding: utf-8
from setuptools import setup

install_requires = []

dev_packages = {
    'dev': [
        'pytest',
        'pytest-cov'
    ]
}

setup(
    name='MZBackup',
    version='0.95',
    description='Migración/Backup de Usuarios y Cuentas en Zimbra',
    author='vtacius',
    author_email='vtacius@gmail.com',
    license='GPLv3',

    packages=[
        'MZBackup',
        'MZBackup.lib',
    ],
    extras_require=dev_packages,
    install_requires=install_requires,

    test_suite="pytest"
)
