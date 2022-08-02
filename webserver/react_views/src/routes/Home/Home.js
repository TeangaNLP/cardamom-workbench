import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import { NavBar } from "../../components";
import axios from "axios";

import "./Home.css";

const Home = (props) => {
  const [isLoading, setIsLoading] = useState(true);
  const [documents, setDocuments] = useState([]);
  const navigate = useNavigate();

  const userId = props.userId;

  useEffect(() => {
    // Update the document title using the browser API
    if (!userId) {
      navigate("/login", { replace: true });
    }

    axios
      .get("http://localhost:5001/api/get_files?user=" + userId)
      .then(function (response) {
        console.log(response);
        setDocuments(response.data.file_contents);
        setIsLoading(false);
      })
      .catch(function (err) {
        console.log(err);
      });
  }, []);

  return (
    <div>
      <NavBar pages={[{ path: "/", name: "Home" }, { path: "/fileupload", name: "File Upload" }]} />
      {isLoading ? <div>Loading...</div> : documents.length > 0 ? (
        documents.map(doc => {
          return (
            <ListGroup key={doc.filename} className="list-item">
              <ListGroup.Item
                action
                onClick={() => {
                  navigate("/tokeniser");
                  props.setFileInfo({ fileId: doc.file_id, content: doc.content, langId: doc.lang_id });
                }
                }
              >
                {doc.filename}
              </ListGroup.Item>
            </ListGroup>);
        })
      ) : <div>No Documents Uploaded!</div>}
    </div>
  );
};

export default Home;
