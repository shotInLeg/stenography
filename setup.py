from setuptools import setup, find_packages

print(find_packages())

setup(
    name='stenography',
    packages=find_packages(),
    install_requires=[],
    version='0.0.1',
    description='Multifunctional logging module',
    keywords='logging, logger',
    url='https://github.com/shotInLeg/stenography',
    download_url='https://github.com/shotInLeg/stenography/archive/0.1.1.tar.gz',
    author='Anton Zvonarev (shotinleg)',
    author_email='shotinleg@yandex.ru',
    license='GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007',
    long_description='Multifunctional logging module',
    include_package_data=True
)
