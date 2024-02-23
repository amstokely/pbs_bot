from setuptools import setup, Extension, find_packages
import os

# Define the extension module for SWIG
path = os.path.dirname(os.path.abspath(__file__)) + '/'
secrets_extension = Extension(
    'pbs_bot.secrets._secrets',  # Name of the module
    sources=[path + 'src/pbs_bot/secrets/secrets.i',
             path + 'src/pbs_bot/secrets/secrets.cc'],  # SWIG
    # interface file
    # and the C source file
    swig_opts=['-c++'],  # SWIG options for Python 3 and modern
    # C++
)


setup(
    name='pbs_bot',  # Name of your package
    version='0.1.0',  # Version number
    packages=find_packages(where='src'),  # Packages to include
    package_dir={'': 'src'},  # Directory of the source code
    ext_modules=[secrets_extension],  # Extension modules (SWIG)
    python_requires='>=3.8',  # Minimum version requirement of the
    # Python programming language
)

