from abc import ABC, abstractmethod

class AbstractUnitOfWork(ABC):
    """
    Abstract base class defining the interface for a unit of work pattern.
    """
    def __enter__(self):
        """
        Enter method for context management.
        """
        return self

    def __exit__(self, *args):
        """
        Exit method for context management, performs rollback by default.
        """
        self.rollback()

    @abstractmethod
    def commit(self):
        """
        Abstract method to commit changes in the unit of work.
        """
        pass

    @abstractmethod
    def rollback(self):
        """
        Abstract method to rollback changes in the unit of work.
        """
        pass

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """
    Implementation of AbstractUnitOfWork using SQLAlchemy session.
    """
    def __init__(self, session_factory, repository_class):
        """
        Initialize SqlAlchemyUnitOfWork with session factory and repository class.

        Args:
            session_factory (function): A function that creates a new SQLAlchemy session.
            repository_class (type): The class of the repository to be instantiated.
        """
        self.session_factory = session_factory
        self.repository_class = repository_class

    def __enter__(self):
        """
        Enter method for context management. Opens a new session and initializes repository.
        """
        self.session = self.session_factory()
        self.repo = self.repository_class(self.session)
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit method for context management. Closes the session.
        """
        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.close()

    def commit(self):
        """
        Commit changes in the current session.
        """
        self.session.commit()
    def flush(self):
        self.session.flush()

    def rollback(self):
        """
        Rollback changes in the current session.
        """
        self.session.rollback()
    def close(self):
        self.session.close()
