from setuptools import setup, find_packages
from pathlib import Path
import toml

# Path to the .bumpversion.toml file
bumpversion_file = Path(__file__).parent / '.bumpversion.toml'

# Read the .bumpversion.toml file and extract the version
bumpversion_data = toml.load(bumpversion_file)
current_version = bumpversion_data['tool']['bumpversion']['current_version']

setup(
    name='riscvflow',
    version=current_version,
    description='A library for control flow graph analysis of RISC-V assembly',
    author='Akshit Sharma',
    author_email='akshitsharma@mines.edu',
    packaes=find_packages(),
    install_requires=[
    ],
)
