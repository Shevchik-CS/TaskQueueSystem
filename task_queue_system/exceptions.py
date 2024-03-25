"""
Custom exception classes for TaskQueueSystem
"""


class TaskQueueException(Exception):
    """Custom exception for TaskQueue related errors."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
