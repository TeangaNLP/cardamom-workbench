import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import { NavBar } from "../../components";
import axios from "axios";

import "./Home.css";

const Home = (props) => {
  const [documents, updateDocuments] = useState([]);
  const navigate = useNavigate();

  const userId = props.userId;
  console.log(userId);

  const buildDocuments = (docs) => {
    console.log(docs);
    let newDocs = [];
    for (const doc of docs) {
      console.log(doc);
      newDocs.push(
        <ListGroup key={doc.filename} className="list-item">
          <ListGroup.Item
            action
            onClick={() =>
              navigate("/tokeniser", { state: { data: doc.content } })
            }
          >
            {doc.filename}
          </ListGroup.Item>
        </ListGroup>
      );
    }
    updateDocuments(newDocs);
  };

  useEffect(() => {
    // Update the document title using the browser API

    console.log(userId);
    if (!userId) {
      navigate("/login", { replace: true });
    }

    const data = new FormData();
    data.append("user", userId);

    axios
      .get("http://localhost:5001/api/file?user=" + userId)
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
};

export default Home;
