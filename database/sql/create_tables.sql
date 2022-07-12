CREATE DATABASE workbench; 

\c workbench;

CREATE TABLE IF NOT EXISTS users (
  id SERIAL NOT NULL,
  name varchar(250) NOT NULL,
  email varchar(250) NOT NULL,
  password varchar NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS languages (
  id SERIAL NOT NULL,
  PRIMARY KEY (id),
  language_name varchar(250) NOT NULL,
  iso_code varchar(250),
  requested boolean NOT NULL
);

CREATE TABLE IF NOT EXISTS uploaded_files (
  id SERIAL NOT NULL,
  name varchar(250) NOT NULL,
  content varchar NOT NULL,
  PRIMARY KEY (id),
  user_id serial NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  language_id integer,
  FOREIGN KEY (language_id) REFERENCES languages(id)
);

CREATE TABLE IF NOT EXISTS provenance (
  id SERIAL NOT NULL,
  timestamp varchar(250) NOT NULL,
  reference_id integer
);

CREATE TABLE IF NOT EXISTS annotations (
  id SERIAL NOT NULL,
  token varchar(10000) NOT NULL,
  reserved_token boolean NOT NULL,
  start_index integer NOT NULL,
  end_index integer NOT NULL,
  token_language_id integer,
  FOREIGN KEY (token_language_id) REFERENCES languages(id),
  type varchar(250) NOT NULL,
  PRIMARY KEY (id),
  uploaded_file_id serial NOT NULL,
  FOREIGN KEY (uploaded_file_id) REFERENCES uploaded_files(id) ON DELETE CASCADE
);



/*INSERT INTO uploaded_file (name, content) VALUES ('a-filename.pdf', 'this is a content');*/ 
