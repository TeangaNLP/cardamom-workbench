CREATE DATABASE files; 

\c files;

CREATE TABLE IF NOT EXISTS uploaded_file (
  file_id SERIAL NOT NULL,
  name varchar(250) NOT NULL,
  content varchar NOT NULL,
  PRIMARY KEY (file_id)
);

/*INSERT INTO uploaded_file (name, content) VALUES ('a-filename.pdf', 'this is a content');*/ 
