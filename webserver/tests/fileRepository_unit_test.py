import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import UploadedFileModel, LanguageModel, UserModel
from repositories.fileRepository import FileRepository
from orm import Base, start_mappers
import config

# Call start_mappers to ensure SQLAlchemy mappings are initialized
start_mappers()

class TestFileRepository(unittest.TestCase):
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
        Set up a session and FileRepository instance for each test.
        """
        self.session = self.Session()
        self.file_repository = FileRepository(self.session)
        self.new_file = UploadedFileModel(name="Test File", content="Example file content", user_id=1, language_id=1)
        self.new_file_id = 9
    
    def tearDown(self):
        """
        Roll back any changes and close the session after each test.
        """
        self.session.rollback()
        self.session.close()

    def test_1_add_file(self):
        """
        Test adding a file to the database.
        """
        # Create a new file instance

        # Add the new file to the database
        file = self.file_repository.add(self.new_file.name, self.new_file.content, self.new_file.user_id, self.new_file.language_id)
        self.new_file_id = file.id  # Assign the ID of the newly added file to a class attribute

    def test_2_get_file_by_id(self):
        """
        Test retrieving a file by its ID from the database.
        """

        # Retrieve the file by its ID
        retrieved_file = self.file_repository.get(self.new_file_id)

        # Assert that the retrieved file matches the added file
        self.assertEqual(retrieved_file.name, "Test File")
        self.assertEqual(retrieved_file.content, "Example file content")
        self.assertEqual(retrieved_file.user_id, 1)
        self.assertEqual(retrieved_file.language_id, 1)

    def test_get_all_files_by_user_id(self):
        """
        Test retrieving all files associated with a specific user ID.
        """
        # Add files for different users
        user1_id = 2  # Replace with an existing user ID from your test database
        user2_id = 3  # Replace with another existing user ID from your test database

        # Add files for user 1
        self.file_repository.add("File 1 for User 2", "Content 1", user1_id, 1)
        self.file_repository.add("File 2 for User 2", "Content 2", user1_id, 1)
        # Add files for user 2
        self.file_repository.add("File 1 for User 3", "Content 3", user2_id, 1)

        # Retrieve files for user 1
        files_user1 = self.file_repository.get_all(user1_id).uploaded_files
        actual_number = len(files_user1)
        # Assert the number and details of files retrieved for user 1
        self.assertEqual(actual_number, 2)
        self.assertEqual(files_user1[0].name, "File 1 for User 2")
        self.assertEqual(files_user1[1].name, "File 2 for User 2")

    def test_get_language_by_iso_code(self):
        """
        Test retrieving a language by its ISO code from the database.
        """
        # Add a language
        iso_code = "en"
        language_name = "English"

        # Retrieve the language by its ISO code
        retrieved_language = self.file_repository.get_language_by_iso_code(iso_code)

        # Assert that the retrieved language matches the added language
        self.assertEqual(retrieved_language.iso_code, iso_code)
        self.assertEqual(retrieved_language.name, language_name)

if __name__ == '__main__':
    unittest.main()

