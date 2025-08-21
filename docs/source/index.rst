knit-script
===========

.. image:: https://img.shields.io/pypi/v/knit-script.svg
   :target: https://pypi.org/project/knit-script/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/knit-script.svg
   :target: https://pypi.org/project/knit-script
   :alt: Python Version

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

.. image:: https://img.shields.io/badge/type_checker-mypy-blue.svg
   :target: https://mypy-lang.org/
   :alt: Code style: MyPy

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: Pre-commit

KnitScript is a domain-specific programming language for writing V-bed knitting machine instructions.
The language is loosely based on conventions from Python 3 but includes support for controlling a knitting machine.
The code is interpreted into knitout which can then be processed into instructions for different types of knitting machines.

🧶 Overview
-----------

KnitScript is a domain-specific programming language designed to make knitting machine programming accessible and intuitive.
While traditional knitout requires low-level instruction management, KnitScript provides:

- **High-level abstractions** for common knitting patterns
- **Automatic optimization** of needle operations and carriage passes
- **Python-like syntax** familiar to programmers
- **Multi-sheet support** for complex fabric structures
- **Comprehensive error handling** with detailed diagnostics

The language compiles to standard knitout format, making it compatible with any machine that supports the knitout specification.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :hidden:

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: Language Guide
   :hidden:

   language_reference
   machine_operations

.. toctree::
   :maxdepth: 4
   :caption: API Reference
   :hidden:

   api/knit_script

.. toctree::
   :maxdepth: 1
   :caption: Project Information
   :hidden:

   dependencies
   related_projects
   acknowledgments
