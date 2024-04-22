class UserModel():
    '''
    The User data model

    Parameters
    ----------
    name: str
        the user name

    email: str
        the user email str

    password: str
        the user given raw str

    Returns
    -------
    dict
        a dict of attributes name and their values

    Examples
    -------
    user = UserModel(name='Laura',
                     email='laura@gmail.com',
                     password='123')
    Raises
    ------
    should raise error if not data class

    Side-effect
    ----------
    no side effects
    '''
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class UploadedFileModel():
    def __init__(self, name, content, user_id, language_id):
        self.name = name
        self.content = content
        self.user_id = user_id
        self.language_id = language_id

class LanguageModel():
    def __init__(self, language_name, iso_code, requested):
        self.language_name = language_name
        self.iso_code = iso_code
        self.requested = requested

class ProvenanceModel():
    def __init__(self, timestamp, reference_id):
        self.timestamp = timestamp
        self.reference_id = reference_id

class POSInstanceModel():
    def __init__(self, token_id, tag, type_):
        self.token_id = token_id
        self.tag = tag
        self.type_ = type_

class POSFeaturesModel():
    def __init__(self, posinstance_id, feature, value):
        self.posinstance_id = posinstance_id
        self.feature = feature
        self.value = value

class TokenModel():
    def __init__(self, reserved_token, start_index, end_index, token_language_id, type_, uploaded_file_id):
        self.reserved_token = reserved_token
        self.start_index = start_index
        self.end_index = end_index
        self.token_language_id = token_language_id
        self.type_ = type_
        self.uploaded_file_id = uploaded_file_id

class RelatedWordModel():
    def __init__(self, query, query_language, model_name, word, similarity_score):
        self.query = query
        self.query_language = query_language
        self.model_name = model_name
        self.word = word
        self.similarity_score = similarity_score

class SpaceModel():
    def __init__(self, space_index, space_type, uploaded_file_id):
        self.space_index = space_index
        self.space_type = space_type
        self.uploaded_file_id = uploaded_file_id
