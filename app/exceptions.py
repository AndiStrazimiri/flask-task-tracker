# app/exceptions.py

class NotFoundError(Exception):
    """Raised when an entity is not found."""
    pass

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

class RepositoryError(Exception):
    """Raised when repository/database operation fails."""
    pass
