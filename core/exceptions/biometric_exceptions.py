"""Biometric algorithm exceptions."""


class BiometricException(Exception):
    """Base exception for biometric operations."""
    pass


class AlgorithmTimeoutError(BiometricException):
    """Algorithm execution timeout."""
    pass


class InvalidInputError(BiometricException):
    """Invalid input for algorithm."""
    pass


class AlgorithmError(BiometricException):
    """Algorithm execution error."""
    pass

