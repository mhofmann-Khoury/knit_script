"""Logger configuration for KnitScript test cases.

This module provides pre-configured loggers that automatically adapt to the execution environment.
In headless environments (like GitHub Actions), loggers are silenced to keep test output clean.
In interactive environments, loggers output to the console for local debugging.
"""

import os

from knit_script.knit_script_interpreter.knitscript_logging.knitscript_logger import Knit_Script_Logger, KnitScript_Debug_Log, KnitScript_Error_Log, KnitScript_Logging_Level, KnitScript_Warning_Log


def _is_headless_environment() -> bool:
    """
    Detect if running in a headless environment (CI/CD).

    Returns:
        bool: True if in a headless environment, False otherwise.
    """
    # Check common CI environment variables
    ci_indicators = [
        "CI",  # Generic CI indicator
        "GITHUB_ACTIONS",  # GitHub Actions
        "TRAVIS",  # Travis CI
        "CIRCLECI",  # Circle CI
        "JENKINS_HOME",  # Jenkins
        "GITLAB_CI",  # GitLab CI
        "BUILDKITE",  # Buildkite
        "TF_BUILD",  # Azure Pipelines
    ]

    return any(os.environ.get(indicator) for indicator in ci_indicators)


# Determine logging configuration based on environment
_log_to_console = not _is_headless_environment()


def get_test_info_logger(name: str = "Test KnitScript Log", to_file: bool = False) -> Knit_Script_Logger:
    """
    Args:
        name (str, optional): Name of logger to use. Defaults to "Test KnitScript Log".
        to_file (bool, optional): Whether to write to file. Defaults to False.

    Returns:
        Knit_Script_Logger: Knit_Script_Logger used for a given test case.
    """
    return Knit_Script_Logger(log_to_console=_log_to_console, log_to_file=to_file, logging_level=KnitScript_Logging_Level.info, log_name=name)


def get_test_warning_logger(name: str = "Test KnitScript Warning Log", to_file: bool = False) -> KnitScript_Warning_Log:
    """
    Args:
        name (str, optional): Name of logger to use. Defaults to "Test KnitScript Warning Log".
        to_file (bool, optional): Whether to write to file. Defaults to False.

    Returns:
        KnitScript_Warning_Logger: Knit_Script_Warning_Logger used for a given test case.
    """
    return KnitScript_Warning_Log(log_to_console=_log_to_console, log_to_file=to_file, log_name=name)


def get_test_error_logger(name: str = "Test KnitScript Error Log", to_file: bool = False) -> KnitScript_Error_Log:
    """
    Args:
        name (str, optional): Name of logger to use. Defaults to "Test KnitScript Error Log".
        to_file (bool, optional): Whether to write to file. Defaults to False.

    Returns:
        KnitScript_Error_Logger: Logger used for a given test case.
    """
    return KnitScript_Error_Log(log_to_console=_log_to_console, log_to_file=to_file, log_name=name)


def get_test_debug_logger(name: str = "Test KnitScript Debug Log", to_file: bool = False) -> KnitScript_Debug_Log:
    """
    Args:
        name (str, optional): Name of logger to use. Defaults to "Test KnitScript Debug Log".
        to_file (bool, optional): Whether to write to file. Defaults to False.

    Returns:
        KnitScript_Debug_Logger: Logger used for a given test case.
    """
    return KnitScript_Debug_Log(log_to_console=_log_to_console, log_to_file=to_file, log_name=name)
