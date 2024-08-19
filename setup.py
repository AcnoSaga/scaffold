from setuptools import setup, find_packages

setup(
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        'scaffold': ['templates/*/Dockerfile', 'templates/*/*'],
    },
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'scaffold=scaffold.main:main',
        ],
    },
)