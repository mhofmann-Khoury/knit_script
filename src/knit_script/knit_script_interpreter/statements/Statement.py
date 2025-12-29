"""Basic statement structures.

This module provides the base Statement class and the Expression_Statement class, which form the foundation of the knit script statement system.
These classes define the basic contract for executable code elements and provide mechanisms for using expressions as statements.
"""

from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.ks_element import KS_Element, associate_error


class Statement(KS_Element):
    """Superclass for all operations that do not produce a value.

    This is the base class for all executable statements in the knit script language. Statements perform actions or side effects but do not return values (unlike expressions).
    They represent the fundamental building blocks of knit script programs and define the contract that all executable code elements must follow.

    The Statement class extends KS_Element to provide execution capabilities while maintaining access to parser node information for error reporting and debugging.
    All specific statement types inherit from this class and implement the execute method to define their behavior.
    """

    def __init__(self, parser_node: LRStackNode):
        """Initialize a statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
        """
        super().__init__(parser_node)

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Automatically wrap execute methods in subclasses with appropriate error handling and debugging decorators.

        This method is called whenever a class inherits from Statement.
        It checks if the subclass defines its own execute method and wraps it with the appropriate decorators

        Args:
            **kwargs (Any): Additional keyword arguments passed to super().__init_subclass__
        """
        super().__init_subclass__(**kwargs)

        # Check if this subclass defines its own execute or evaluate method (not inherited)
        if "execute" in cls.__dict__:
            original_execute = cls.__dict__["execute"]
            if not hasattr(original_execute, "__wrapped__"):
                wrapped_execute = associate_error(original_execute)
                cls.execute = wrapped_execute  # type: ignore[method-assign]

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the statement at the current machine context.

        This is the main method that subclasses override to implement their specific behavior. The base implementation does nothing and should be overridden by all concrete statement types.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.

        Raises:
            NotImplementedError: The base implementation does not implement the execute method.
        """
        raise NotImplementedError
