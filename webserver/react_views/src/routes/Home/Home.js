import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import { NavBar } from "../../components";
import axios from "axios";

import "./Home.css";

const Home = ({
                user,
		setUser,
                documents,
                setDocuments,
                setFileInfo,
		setUserId
              }) => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const r = () => { 
      const userId = user.id;
      axios
      .get("http://localhost:5001/api/get_files?user=" + userId)
      .then(function (response) {
	const documents = response.data.file_contents
        setDocuments(documents);
	setUser({...user, documents:documents});
	localStorage.setItem('user', JSON.stringify(user));
        setIsLoading(false);
      })
      .catch(function (err) {
        console.log(err);
      }); }


    useEffect(() => {
	/*if(user.documents){
		setIsLoading(false);
		setDocuments(user.documents)
		return
	}*/
	r()
    },[])
  /*useEffect(() => {
    // Update the document title using the browser API
    if (userId === undefined && localStorage.getItem('userId') === null) {
      navigate("/login", { replace: true });
    }
    else if(userId === undefined && localStorage.getItem('userId') !== null){
      setUserId(localStorage.getItem('userId'));
    }
    r();

  }, [userId]);*/

  return (
    <div>
      <NavBar setUser={setUser} pages={[{ path: "/", name: "Home" }, { path: "/fileupload", name: "File Upload" }]} />
      <h1> Welcome {user.name} </h1>
      {isLoading ? <div>Loading...</div> : documents.length > 0 ? (
        documents.map(doc => {
          return (
            <ListGroup key={doc.filename} className="list-item">
              <ListGroup.Item
                action
                onClick={() => {
                  setFileInfo({
                    ...doc
                  })
                  navigate(`/tokeniser/${doc.filename}`)
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
