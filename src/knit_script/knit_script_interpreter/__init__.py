"""
Knit Script Interpreter Package
===============================

This package provides the core interpreter infrastructure for the Knit Script language, handling parsing, execution context management, and code generation.

Core Components
---------------

Interpreter Classes:
    Knit_Script_Interpreter: Main interpreter class that orchestrates parsing and execution of knit script programs.
    Knit_Script_Context: Manages execution state, variable scopes, and machine interaction during program execution.

Parser Infrastructure:
    Knit_Script_Parser: Concrete parser implementation using parglare library.
    knit_script_actions: Action functions for converting parse tree nodes into executable knit script elements.

Base Classes:
    KS_Element: Superclass for all knit script language elements, providing location tracking and common functionality.

Architecture Overview
---------------------

The interpreter follows a multi-stage execution model:

1. **Parsing Stage**: Source code is parsed into an abstract syntax tree using the parglare parser generator with custom grammar rules.

2. **Context Setup**: Execution context is established with machine state, variable scopes, and knitout generation infrastructure.

3. **Execution Stage**: Statements are executed in order, manipulating machine state and generating knitout instructions.

4. **Output Generation**: Final knitout instructions are written to files and knit graphs are generated for visualization.

Key Features
------------

Language Processing:
    - Complete knit script grammar implementation
    - Action-based parse tree transformation
    - Error handling and location tracking
    - Module import system support

Execution Management:
    - Hierarchical variable scoping
    - Machine state synchronization
    - Knitout instruction generation
    - Context isolation for functions and modules

Machine Integration:
    - Direct virtual machine manipulation
    - Gauge and sheet management
    - Carrier and yarn control
    - Needle operation coordination

Output Generation:
    - Knitout format compliance
    - Knit graph visualization
    - Error recovery and debugging support
    - Performance optimization

Error Handling:
    - Comprehensive exception system
    - Location-aware error reporting
    - Graceful failure recovery
    - Debug output generation


"""
