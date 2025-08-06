Dependencies
============

Complete overview of KnitScript's dependencies and version requirements.

🐍 Python Version Requirements
------------------------------

KnitScript requires **Python 3.11 or 3.12**.

**Supported Python Versions:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - 3.11
     - ✅ Supported
     - Improved performance
   * - 3.12
     - ✅ Supported
     - Latest features and optimizations

📦 Runtime Dependencies
-----------------------

Core Dependencies
~~~~~~~~~~~~~~~~~

These packages are automatically installed with KnitScript:

**parglare** (^0.18.0)
   Parser generator library used for KnitScript grammar parsing and syntax analysis.

   - Provides LR/GLR parsing capabilities
   - Handles KnitScript grammar definition
   - Generates detailed parse trees for error reporting

**knit-graphs** (^0.0.6)
   Knitting graph data structures for representing fabric topology.

   - Models stitch relationships and fabric structure
   - Provides analysis tools for knitted fabrics
   - Enables pattern validation and optimization

**virtual-knitting-machine** (^0.0.13)
   Virtual machine simulation for knitting operations.

   - Simulates V-bed knitting machine behavior
   - Tracks machine state during pattern execution
   - Validates machine operations and constraints

**knitout-interpreter** (^0.0.18)
   Knitout processing and execution framework.

   - Processes generated knitout instructions
   - Provides instruction validation and optimization
   - Handles knitout format compliance

**importlib_resources** (^6.5.0)
   Resource management for grammar files and templates.

   - Manages KnitScript grammar files
   - Handles template and resource loading
   - Provides cross-platform resource access

For more information about the broader knitting software ecosystem, see :doc:`related_projects`.
