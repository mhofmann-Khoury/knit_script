Related Projects
================

KnitScript is part of a broader ecosystem of knitting software and research projects. This page provides an overview of related tools, libraries, and research initiatives.

🧶 Northeastern ACT Lab Knitting Ecosystem
------------------------------------------

KnitScript is developed as part of the Northeastern University ACT Lab's comprehensive knitting software ecosystem. These projects work together to provide end-to-end knitting machine programming capabilities.

Core Knitting Libraries
~~~~~~~~~~~~~~~~~~~~~~~

**knit-graphs** |knit_graphs_version|
   Knitting graph data structures and analysis tools.

   - **Purpose**: Models fabric topology and stitch relationships
   - **Key Features**: Stitch dependency tracking, fabric analysis, pattern validation
   - **Integration**: Used by KnitScript to represent generated fabric structures
   - **Repository**: `knit-graphs on PyPI <https://pypi.org/project/knit-graphs/>`_

**virtual-knitting-machine** |vkm_version|
   A simulation of a knitting machine.

   - **Purpose**: Used to verify knitting operations and construct knit graphs.
   - **Repository**: `virtual-knitting-machine on PyPI <https://pypi.org/project/virtual-knitting-machine/>`_

**knit-script** |ks_version|
   A general purpose machine knitting langauge

   - **Purpose**: Fully programmatic support to control knitting machines.
   - **Repository**: `knit-script on PyPI <https://pypi.org/project/knit-script/>`_

**knitout-interpreter** |knitout_interp_version|
   Knitout processing and execution framework.

   - **Purpose**: Processes and validates knitout instruction files
   - **Key Features**: Instruction parsing, carriage pass organization, error detection
   - **Integration**: Processes KnitScript's generated knitout output
   - **Repository**: `knitout-interpreter on PyPI <https://pypi.org/project/knitout-interpreter/>`

Optimization and Analysis Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**koda-knitout** |koda_version|
   Optimization framework for knitout instructions.

   - **Purpose**: Optimizes knitout files for faster execution and better quality
   - **Key Features**: Carriage pass optimization, instruction reordering, resource minimization
   - **Integration**: Can post-process KnitScript's generated knitout for optimization
   - **Repository**: `koda-knitout on PyPI <https://pypi.org/project/koda-knitout/>`_

.. |knit_graphs_version| image:: https://img.shields.io/pypi/v/knit-graphs.svg
   :target: https://pypi.org/project/knit-graphs/

.. |ks_version| image:: https://img.shields.io/pypi/v/knit-script.svg
   :target: https://pypi.org/project/knit-script/

.. |vkm_version| image:: https://img.shields.io/pypi/v/virtual-knitting-machine.svg
   :target: https://pypi.org/project/virtual-knitting-machine/

.. |knitout_interp_version| image:: https://img.shields.io/pypi/v/knitout-interpreter.svg
   :target: https://pypi.org/project/knitout-interpreter/

.. |koda_version| image:: https://img.shields.io/pypi/v/koda-knitout.svg
   :target: https://pypi.org/project/koda-knitout/
