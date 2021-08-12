#
# BEST-AIR exception classes
#
class BestAirException(Exception):
    """
    Base exception for BEST-AIR
    """
    pass

class BestAirStopIteration(Exception):
    """
    Thrown when iterations have reached max_iterations or a defined change
    variable has changed less than iteration_epsilon between iterations.
    """
    def __init__(self, reason):
        self.reason = reason

class FileFormatError(BestAirException):
    """
    Indicate a syntax error in a user-managed file.
    """
    pass

class ConfigFileError(FileFormatError):
    """
    Raised for errors in user's configuration file.
    """
    pass

class CommandlineError(BestAirException):
    """
    Command-line arguments were missing or incorrectly specified.
    """
    pass
