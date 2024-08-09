import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import UploadedFileModel, TokenModel, POSInstanceModel
from repositories.posRepository import POSRepository
from orm import Base, start_mappers
import config

# Call start_mappers to ensure SQLAlchemy mappings are initialized
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
        """
        self.session = self.Session()
        self.pos_repository = POSRepository(self.session)

        # Add an existing file
        self.existed_file = UploadedFileModel(
            name="Test File",
            content="Example file content",
            user_id=1,
            language_id=32
        )
        self.session.add(self.existed_file)
        self.session.flush()

        # Add an existing token
        self.existing_token = TokenModel(
            reserved_token=True,
            start_index=0,
            end_index=3,
            token_language_id=32,
            type_="manual",
            uploaded_file_id=self.existed_file.id
        )
        self.session.add(self.existing_token)
        self.session.flush()

    def tearDown(self):
        """
        Roll back any changes and close the session after each test.
        """
        self.session.rollback()
        self.session.close()

    def test_get_tokens(self):
        """
        Test retrieving tokens by file ID from the database.
        """
        tokens = self.pos_repository.get_tokens(self.existed_file.id)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].start_index, self.existing_token.start_index)
        self.assertEqual(tokens[0].end_index, self.existing_token.end_index)
        self.assertEqual(tokens[0].type_, self.existing_token.type_)
        self.assertEqual(tokens[0].uploaded_file_id, self.existed_file.id)

    def test_add_pos_instance(self):
        """
        Test adding a POS instance to the database.
        """
        token_id = self.existing_token.id
        tag = "NOUN"
        type_ = "manual"

        pos_instance = self.pos_repository.add_pos_instance(token_id, tag, type_)
        self.assertIsNotNone(pos_instance.id)
        self.assertEqual(pos_instance.token_id, token_id)
        self.assertEqual(pos_instance.tag, tag)
        self.assertEqual(pos_instance.type_, type_)

        # Retrieve the POS instance from the database
        retrieved_pos_instance = self.session.query(POSInstanceModel).filter(POSInstanceModel.id == pos_instance.id).one()
        self.assertEqual(retrieved_pos_instance.token_id, token_id)
        self.assertEqual(retrieved_pos_instance.tag, tag)
        self.assertEqual(retrieved_pos_instance.type_, type_)

if __name__ == '__main__':
    unittest.main()
