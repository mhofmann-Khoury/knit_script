"""Set Up file for project"""
from setuptools import setup, find_packages

setup(
    name='KnitScript',
    version='0.1',
    packages=find_packages(),
    package_dir={"KnitScript": "KnitScript"},
    package_data={"KnitScript": ["*.pg"], "knit_script_interpreter": ["*.pg"]},
    include_package_data=True,
    url='https://github.khoury.northeastern.edu/mhofmann/KnitScript',
    license='MIT',
    author='Megan Hofmann',
    author_email='m.hofmann@northeastern.edu',
    description='Interpreter from KnitScript to Knitout Instructions',
    long_description=open('README.md').read(),
    install_requires=[
        'networkx==2.8.8',
        'parglare==0.16.0',
        'Naked==0.1.32',
    ]
)
