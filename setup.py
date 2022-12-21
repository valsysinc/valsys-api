"""Setup for distribution"""

from distutils.core import setup

from setuptools import find_packages
with open('requirements.txt') as f:
    required = f.read().splitlines()
setup(
    name='valsys',
    packages=find_packages(),
    version="0.4.4",
    license='MIT',
    description='Valsys python library',
    author='Jonathan Pearson',
    author_email='jonathan.pearson@valsys.com',
    url='https://valsys.io/',
    install_requires=required,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6',  # Minimum version requirement of the package
)
