from unit_of_work.unitOfWork import SqlAlchemyUnitOfWork
from utilities import process_txt_file, process_docx_file, serialise_data_model

class FileService:
    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.uow = uow

    def upload_file(self, uploaded_file, user_id, iso_code):
        name = uploaded_file.filename
        name, extension = ".".join(name.split('.')[:-1]), uploaded_file.filename.split('.')[-1]

        with self.uow as uow:
            lang = uow.repo.get_language_by_iso_code(iso_code)
            if not lang:
                raise ValueError("Invalid ISO code")
            if extension == 'txt':
                content = process_txt_file(uploaded_file)
            elif extension == 'docx':
                content = process_docx_file(uploaded_file)
            else:
                raise ValueError("Unsupported file extension")
            
            uow.repo.add(name, content, user_id, lang.id)
            uow.commit()

    def get_all_files(self, user_id):
        with self.uow as uow:
            files_ = uow.repo.get_all_files(user_id)
            file_contents = [{
                "filename": file.name,
                "file_id": file.id,
                "content": file.content.replace("\\n", "\n"),
                "lang_id": file.language_id
            } for file in files_]
            return file_contents

    def get_file_by_id(self, user_id, file_id):
        with self.uow as uow:
            file = uow.repo.get(file_id)
            if file.user_id == user_id:
                file_contents = {
                    "filename": file.name,
                    "file_id": file.id,
                    "content": file.content,
                    "tokens": [{
                        "content": file.content[token.start_index:token.end_index],
                        **serialise_data_model(token)
                    } for token in file.tokens],
                    "lang_id": file.language_id
                }
                response_dict = {"file_contents": file_contents, "message": "successful"}
            else:
                response_dict = {"message": "Requested file is not accessible"}
            uow.commit()
            return response_dict
