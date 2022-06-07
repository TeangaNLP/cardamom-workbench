import model

database = {
    "users":{},
    "files":{},
    "tokens":{},
    "annotations":{}
}

class DbManager():
    def insert_user(self, username, data):
        if not database["users"].get(username, False):
            user = model.User(*data)
            database["users"][username] = user
            return database["users"][username]
        raise Exception("do something to handle inserting user twice")

    def get_user(self, username) :
        if database["users"].get(username, False):
            return database["users"][username]
        raise Exception("do something to handle getting non-existent user")
       
    def insert_file(self, username, data):
        file_ = model.UploadedFile(*data)
        if not database["files"].get(username, False):
            database["files"][username] = [file_]
        else:
            database["files"][username].append(file_)
        return len(database["files"][username])
    
    def get_files(self, username):
        if database["files"].get(username, False):
            return database["files"][username]
        raise Exception("do something to handle getting non-existent file")