"""
Knit Script Gauged Sheet Schema Package
=======================================

This package provides comprehensive sheet and layer management for multi-gauge knitting operations within the Knit Script interpreter.
It handles the complex task of organizing and tracking loop positions across multiple virtual sheets on a knitting machine.

The gauged sheet system enables advanced knitting techniques by:
- Managing multiple virtual sheets within a single gauge configuration.
- Tracking loop positions and states across different needle beds.
- Managing layer ordering and sheet peeling operations.
- Providing automatic loop restoration and validation.
- Supporting both standard and slider needle operations.

Core Components
---------------

Gauged_Sheet_Record:
    The primary orchestrator class that manages multiple sheets within a gauge configuration.
    Handles sheet peeling, layer management, and loop tracking across the entire gauge system.

Sheet:
    Individual sheet representation that tracks loop positions and provides access to needles belonging to that specific sheet within a gauge.

Key Features
------------

Multi-Sheet Management:
    - Create and manage multiple virtual sheets at a given gauge.
    - Maintain sheet-specific needle collections and loop records

Layer Organization:
    - Dynamic layer positioning and reordering.
    - Forward/backward layer pushing operations.
    - Layer swapping between different sheet positions.
    - Front/back layer positioning utilities.

Sheet Peeling Operations:
    - Automatic loop movement to access specific sheets.
    - Conflict detection and resolution during peeling.
    - Knitout instruction generation for machine operations.
    - Prevention of loop loss during sheet transitions.

Loop State Management:
    - Comprehensive loop tracking and validation.
    - Detection of stacked loops and blocking conditions.
    - Automatic loop restoration after sheet operations.
    - Error handling for lost or misplaced loops.

Needle Access Patterns:
    - Sheet-specific needle collections (front/back, standard/slider).
    - Loop-holding needle identification.
    - Cross-sheet needle position mapping.
    - Needle bed organization utilities.

Architecture Overview
---------------------
Sheet Positioning:
- Sheets are numbered from 0 to gauge-1.
- Layer positions determine physical needle placement.
- Lower layer values represent needles closer to the front.
- Layer manipulation affects which sheets are accessible.

Error Handling
--------------

The package includes robust error handling for common knitting scenarios:

- **Lost_Sheet_Loops_Exception**: Raised when loops are lost during operations.
- **Sheet_Peeling_Stacked_Loops_Exception**: When loops are stacked incorrectly.
- **Sheet_Peeling_Blocked_Loops_Exception**: When loops block access to sheets.
- **Sheet_Value_Exception**: For invalid sheet numbers or configurations.
"""
