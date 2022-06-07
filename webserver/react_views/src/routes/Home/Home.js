import { useState, useEffect } from 'react';
import { useLocation, Navigate, NavLink, navigate, useNavigate } from 'react-router-dom';
import { ListGroup } from 'react-bootstrap';
import { NavBar } from '../../components';
import axios from "axios";

import "./Home.css";

const Home = () => {

  const [documents, updateDocuments] = useState([]);
  const navigate = useNavigate();

  const location = useLocation();
  const userAuthenticated = location.state;

  const buildDocuments = (docs) => {
    console.log(docs);
    let newDocs = [];
    for (const doc of docs) {
      console.log(doc);
      newDocs.push(
        <ListGroup key={doc.filename} className='list-item'>
          <ListGroup.Item action onClick={() => navigate("/tokeniser", { state: { data: doc.content } })}>
            {doc.filename}
          </ListGroup.Item>
        </ListGroup>
      )
    }
    updateDocuments(newDocs)
  }

  useEffect(() => {
    // Update the document title using the browser API

    console.log(userAuthenticated)
    if (!userAuthenticated) {
      navigate("/login", { replace: true });
    }

    const data = new FormData()
    data.append("user", userAuthenticated)

    axios
      .get("http://127.0.0.1/api/file?user=" + userAuthenticated)
      .then(function (response) {
        console.log(response);
        buildDocuments(response.data.file_contents);
      })
      .catch(function (err) {
        console.log(err);
      });
  }, []);

  return (
    <div>
      <NavBar />
      {documents.length > 0 ? documents : <div>No Documents Uploaded!</div>}
    </div>
  );
}

export default Home