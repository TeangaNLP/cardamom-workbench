import { useEffect, useState } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css';

import { Token } from "../../components";
import { Navbar, Container, Nav, Button } from 'react-bootstrap'

import "./PosTagging.css";

const Tagging = () => {

  let [annoText, updateAnnoText] = useState([]);
  let [tags, updateTags] = useState([]);

  const location = useLocation();

  useEffect(() => {
        updateAnnoText(location.state.data);
  }, []);

  // Update the state of the token with a tag.
  const updateTagState = (token, tag) => {
    updateTags({...tags, [token]: tag});
  }

  console.log(tags);

  // Create Tokens for textarea.
  let data = [];
  for (let i = 0; i < annoText.length; i++) {
    data.push(<Token key={i} updateTagState={updateTagState} data={annoText[i]} />);
  }

  return (
    <div>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand >Cardamom Workbench</Navbar.Brand>
          <Nav activeKey={location.pathname} className="me-auto">
            <Nav.Link href="/">File Upload
            </Nav.Link>
            <Nav.Link href="/tokenisation">Tokenisation
            </Nav.Link>
            <Nav.Link href="/tagging">Tagging
            </Nav.Link>
          </Nav>
        </Container>
      </Navbar>
      <div className='annotation-area'>
        <div className="annotation-text">
          {data}
        </div>
      </div>
      <div className="annotation-area save-button">
      <Button variant="dark">Save</Button>
      </div>
    </div>
  );
};
export default Tagging;
