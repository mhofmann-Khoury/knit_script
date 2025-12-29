"""A Module containing the Knit_Script_Logger class"""

from enum import Enum
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, FileHandler, Formatter, Logger, StreamHandler, getLogger
from typing import Any


class KnitScript_Logging_Level(Enum):
    """Enumeration of logging levels for Knit_Script_Logger. Wraps the standard logging levels in the logging package."""

    info = INFO
    debug = DEBUG
    warning = WARNING
    error = ERROR
    critical = CRITICAL

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return int(self.value)

    def print(self, message: str, logger: Logger) -> None:
        """
        Prints the message to the appropriate level using the given logger.
        Args:
            message (str): The message to print.
            logger (Logger): The logger to print from.
        """
        if not logger.hasHandlers():
            return
        if self is KnitScript_Logging_Level.info:
            logger.info(message)
        elif self is KnitScript_Logging_Level.debug:
            logger.debug(message)
        elif self is KnitScript_Logging_Level.warning:
            logger.warning(message)
        elif self is KnitScript_Logging_Level.error:
            logger.error(message)
        elif self is KnitScript_Logging_Level.critical:
            logger.critical(message)


class Knit_Script_Logger:
    """
    A wrapping class for custom logging functionality used to control logging from knitscript separate from the python console.
    """

    def __init__(self, log_to_console: bool = True, log_to_file: bool = False, logging_level: KnitScript_Logging_Level = KnitScript_Logging_Level.info, log_name: str = "KnitScript Console") -> None:
        """
        Args:
            log_to_console (bool, optional): If True, the logger will output its contents to the python console. Defaults to True.
            log_to_file (bool, optional): If True, the logger will output its contents to a log file. Defaults to False.
            logging_level (KnitScript_Logging_Level, optional): The logging level of this logger. Defaults to logging information.
            log_name (str, optional): The name of the logger and the log file produced. Defaults to "KnitScript".
        """
        self._level: KnitScript_Logging_Level = logging_level
        self._logger: Logger = getLogger(f"{log_name}")
        self._logger.setLevel(int(logging_level))
        self._formatter: Formatter = Formatter("KS-%(levelname)s:\n%(message)s")
        self._file_handler: FileHandler | None = FileHandler(f"{self.name}.log") if log_to_file else None
        if self._file_handler is not None:
            self._file_handler.setFormatter(self._formatter)
            self._logger.addHandler(self._file_handler)
        self._console_handler: StreamHandler | None = StreamHandler() if log_to_console else None
        if self._console_handler is not None:
            self._console_handler.setFormatter(self._formatter)
            self._logger.addHandler(self._console_handler)
        self._has_printed: bool = False

    @property
    def name(self) -> str:
        """
        Returns:
            str: The name of this logger.
        """
        return self._logger.name

    @property
    def is_info(self) -> bool:
        """
        Returns:
            bool: True if this logs info messages, False otherwise.
        """
        return self._level == KnitScript_Logging_Level.info

    @property
    def is_debug(self) -> bool:
        """
        Returns:
            bool: True if this logs debug messages, False otherwise.
        """
        return self._level == KnitScript_Logging_Level.debug

    @property
    def is_warning(self) -> bool:
        """
        Returns:
            bool: True if this logs warning messages, False otherwise.
        """
        return self._level == KnitScript_Logging_Level.warning

    @property
    def is_error(self) -> bool:
        """
        Returns:
            bool: True if this logs error messages, False otherwise.
        """
        return self._level == KnitScript_Logging_Level.error

    @property
    def is_critical(self) -> bool:
        """
        Returns:
            bool: True if this logs critical messages, False otherwise.
        """
        return self._level == KnitScript_Logging_Level.critical

    def print(self, message: str) -> None:
        """
        Prints the given message using this logger at the set level.
        If this is the first message printed by the logger, it will add a start line to the output.
        Args:
            message (str): The message to print.
        """
        if not self._has_printed:
            self._level.print(f"{'=' * 20}Logging {self.name}{'=' * 20}", self._logger)
            self._has_printed = True
        self._level.print(message, self._logger)


class KnitScript_Warning_Log(Knit_Script_Logger):
    """
    Used for logging warning messages from Knit Script.
    """

    def __init__(self, log_to_console: bool = True, log_to_file: bool = False, log_name: str = "KnitScript Warnings"):
        super().__init__(log_to_console, log_to_file, logging_level=KnitScript_Logging_Level.warning, log_name=log_name)

    def warn(self, warning: RuntimeWarning, source_element: Any) -> None:
        """
        Prints out the given warning message.
        Args:
            warning (RuntimeWarning): The warning message to print.
            source_element (Any): The KS element that is the source of the warning.
        """
        self.print(f"{repr(source_element)}: {warning.__class__.__name__}: {warning}")


class KnitScript_Error_Log(Knit_Script_Logger):
    """
    Used for logging error messages from Knit Script.
    """

    def __init__(self, log_to_console: bool = True, log_to_file: bool = False, log_name: str = "KnitScript Errors"):
        super().__init__(log_to_console, log_to_file, logging_level=KnitScript_Logging_Level.error, log_name=log_name)

    def report_error(self, error: BaseException, source_element: Any) -> None:
        """
        Prints out the given error message.
        Args:
            error (BaseException): The error to report.
            source_element (Any): The KS element that is the source of the error.
        """
        self.print(f"{repr(source_element)}: {error}")


class KnitScript_Debug_Log(Knit_Script_Logger):
    """
    Used for logging debug messages from Knit Script.
    """

    def __init__(self, log_to_console: bool = True, log_to_file: bool = False, log_name: str = "KnitScript Debugger"):
        super().__init__(log_to_console, log_to_file, logging_level=KnitScript_Logging_Level.debug, log_name=log_name)
