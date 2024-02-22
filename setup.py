from setuptools import setup, find_packages

setup(
    name='pbs_bot',
    version='0.1',
    package_dir={'': 'src'},
    # Tells setuptools that packages are under src
    packages=find_packages(where='src'),
    # Tells setuptools to find packages in src
    entry_points={
        'console_scripts': [
            'pbs_bot=main:main',
        ],
    },
    author='Andy Stokely',
    description='A slack bot for managing PBS jobs.',
    install_requires=[
        'slack_sdk',
    ],
    python_requires='>=3.8',
)
