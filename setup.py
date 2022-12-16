"""Set Up file for project"""
from setuptools import setup, find_packages

setup(
    name='knit_script',
    version='0.1.1',
    packages=find_packages(),
    package_dir={"knit_script": "knit_script"},
    package_data={"knit_script": ["*.pg", "*.js"], "knit_script_interpreter": ["*.pg", "*.js"], "": ["*.pg", "*.js"]},
    include_package_data=True,
    url='https://github.com/mhofmann-Khoury/knit_script',
    download_url='https://github.com/mhofmann-Khoury/knit_script.git',
    license='MIT',
    author='Megan Hofmann',
    author_email='m.hofmann@northeastern.edu',
    description='Interpreter from knit_script to Knitout Instructions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'networkx==2.8.8',
        'parglare==0.16.0',
        'Naked==0.1.32',
    ],
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Programming Language :: Python :: 3.9',
                 'Natural Language :: English'],
    entry_points={
        'console_scripts': ['knitscript=knit_script.interpret:main']
    }
)
