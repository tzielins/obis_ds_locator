from setuptools import find_packages, setup

setup(
    name='obis_ds_locator',
    packages=find_packages(include=['obis_ds_locator']),
    version='0.1.0',
    description='Outputs physical locations of datasets',
    author='Tomasz Zielinski',
    license='MIT',
    install_requires=['pybis', 'psycopg2'],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': ['obis_ds_locator=obis_ds_locator.runner:main'],
    }
)