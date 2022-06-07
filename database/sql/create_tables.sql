CREATE DATABASE workbench; 

\c workbench;

CREATE TABLE IF NOT EXISTS users (
  id SERIAL NOT NULL,
  name varchar(250) NOT NULL,
  email varchar(250) NOT NULL,
  password varchar NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS uploaded_files (
  id SERIAL NOT NULL,
  name varchar(250) NOT NULL,
  content varchar NOT NULL,
  PRIMARY KEY (id),
  user_id serial NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS annotations (
  id SERIAL NOT NULL,
  type varchar(250) NOT NULL,
  value varchar(250) NOT NULL,
  PRIMARY KEY (id),
  user_id serial NOT NULL,
  uploaded_file_id serial NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (uploaded_file_id) REFERENCES uploaded_files(id) ON DELETE CASCADE
);

/*INSERT INTO uploaded_file (name, content) VALUES ('a-filename.pdf', 'this is a content');*/ 
