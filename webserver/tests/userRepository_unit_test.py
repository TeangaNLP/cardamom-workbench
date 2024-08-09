import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import UserModel
from repositories.userRepository import UserRepository
from orm import Base, start_mappers
import config

# Call start_mappers to ensure SQLAlchemy mappings are initialized
start_mappers()

class TestUserRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up a test database engine and session factory.
        """
        cls.engine = create_engine(config.get_postgres_uri())
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """
        Set up a session and UserRepository instance for each test.
        """
        self.session = self.Session()
        self.user_repository = UserRepository(self.session)
        # Create a new user instance for each test method
        self.user = UserModel(name="Test User", email="test@example.com", password="test")

    def tearDown(self):
        """
        Roll back any changes and close the session after each test.
        """
        self.session.rollback()
        self.session.close()

    def test_1_add_user(self):
        """
        Test adding a user to the database.
        """
        # Add the user to the database
        self.user_repository.add(self.user)
        self.session.commit()

        # Retrieve the user from the database
        result = self.user_repository.get(self.user.email)

        # Assert the user was added correctly
        self.assertIsNotNone(result)
        self.assertEqual(result.name, self.user.name)
        self.assertEqual(result.email, self.user.email)
        self.assertEqual(result.password, self.user.password)

    def test_2_get_user(self):
        """
        Test retrieving a user by email from the database.
        """
        # Retrieve the user from the database
        result = self.user_repository.get("test@example.com")
        
        # Assert the user was retrieved correctly
        self.assertEqual(result.email, self.user.name)
        self.assertEqual(result.email, self.user.email)
        self.assertEqual(result.password, self.user.password)

    def test_3_delete_user(self):
        """
        Test deleting a user from the database.
        """
        # Delete the user from the database
        self.user_repository.delete("test@example.com")

        # Attempt to retrieve the user again
        result = self.user_repository.get("test@example.com")

        # Assert that the user was deleted
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
