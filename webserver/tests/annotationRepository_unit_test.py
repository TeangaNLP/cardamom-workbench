import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import UploadedFileModel, TokenModel, LanguageModel
from repositories.annotationRepository import AnnotationRepository
from orm import Base, start_mappers
import config

# Start the mappers
start_mappers()

class TestAnnotationRepository(unittest.TestCase):
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
        Set up a session and AnnotationRepository instance for each test.
        Initialize the database with test data.
        """
        self.session = self.Session()
        self.annotation_repository = AnnotationRepository(self.session)

        self.file_id = 1
        self.token = TokenModel( reserved_token=False, start_index=0, end_index=3, token_language_id=32, type_="auto", uploaded_file_id=1)
        self.token.id = 3203
        self.new_token = None
    def tearDown(self):
        """
        Roll back any changes and close the session after each test.
        """
        self.session.rollback()
        self.session.close()

    def test_1_get(self):
        """
        Test retrieving all tokens associated with a file ID from the database.
        """
        file_id = self.file_id
        retrieved_tokens = self.annotation_repository.get(file_id)
        self.assertEqual(retrieved_tokens[0].id, self.token.id)
        self.assertEqual(retrieved_tokens[0].start_index, self.token.start_index)
        self.assertEqual(retrieved_tokens[0].end_index, self.token.end_index)
        self.assertEqual(retrieved_tokens[0].token_language_id, self.token.token_language_id)
        self.assertEqual(retrieved_tokens[0].type_, self.token.type_)
        self.assertEqual(retrieved_tokens[0].uploaded_file_id, self.token.uploaded_file_id)
    def test_2_add(self):
        """
        Test adding a new token to the database and comparing it with the existing token.
        """
        # Add a new token
        annotation_data = {
            "reserved_token": False,
            "start_index": 0,
            "end_index": 3,
            "token_language_id": 32,
            "type_": "auto", 
            "uploaded_file_id": 9
        }

        # Add an existing file
        existed_file = UploadedFileModel(
            name="Test File",
            content="Example file content",
            user_id=1,
            language_id=1  # Updated to match token_language_id
        )

        new_token_to_add = self.annotation_repository.add(annotation_data, self.annotation_repository.get_file_by_id(9), 9)

        # Retrieve tokens by file ID
        retrieved_tokens = self.annotation_repository.get(annotation_data["uploaded_file_id"])

        # Print the start index for debugging
        print(new_token_to_add.end_index)
        print(retrieved_tokens[0].start_index)

        # Assert that the first element matches the token we added
        self.assertEqual(retrieved_tokens[0].reserved_token, new_token_to_add.reserved_token)
        self.assertEqual(retrieved_tokens[0].start_index, new_token_to_add.start_index)
        self.assertEqual(retrieved_tokens[0].end_index, new_token_to_add.end_index)
        self.assertEqual(retrieved_tokens[0].token_language_id, new_token_to_add.token_language_id)
        self.assertEqual(retrieved_tokens[0].type_, new_token_to_add.type_)
        self.assertEqual(retrieved_tokens[0].uploaded_file_id, new_token_to_add.uploaded_file_id)


if __name__ == '__main__':
    unittest.main()
