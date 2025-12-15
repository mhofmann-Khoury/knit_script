""" Private helper functions for tracking the stack level of warnings in this library"""

import inspect


def get_user_warning_stack_level_from_knitscript_package() -> int:
    """
    Returns:
        int: The stack level pointing to first caller outside this library.
    """
    # Get the root package name
    package_name = __name__.split(".")[0]  # e.g., "knitout_interpreter"

    frame = inspect.currentframe()
    if frame is None:  # Some Python implementations might not support frames
        return 2  # Reasonable default

    try:
        stack_level = 0
        while frame:
            # Get the module name from the frame's globals
            frame_module = frame.f_globals.get("__name__", "")

            # Check if this frame is from our package
            if not frame_module.startswith(package_name + ".") and frame_module != package_name:
                # This frame is outside our package!
                return stack_level

            stack_level += 1
            frame = frame.f_back

        return stack_level if stack_level > 0 else 2
    finally:
        # Clean up frame reference to avoid reference cycles
        del frame
