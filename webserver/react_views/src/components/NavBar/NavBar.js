import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Container, Nav } from 'react-bootstrap';

import 'bootstrap/dist/css/bootstrap.css';
import "./NavBar.css";

const NavBar = () => {

  const [id, setID] = useState('home');
  const handleActive = (id) => {
    setID(id);
  };

  return (
    <div>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand >Cardamom Workbench</Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link onClick={() => handleActive('home')} className={id == "home" ? "active" : ''} as={Link} to='/'>Home
            </Nav.Link>
            <Nav.Link onClick={() => handleActive('fileupload')} className={id == "fileupload" ? "active" : ''} as={Link} to='/fileupload'>File Upload
            </Nav.Link>
            <Nav.Link onClick={() => handleActive('tokeniser')} className={id == "tokeniser" ? "active" : ''} as={Link} to='/tokeniser' >Tokenisation
            </Nav.Link>
            <Nav.Link onClick={() => handleActive('postagging')} className={id == "postagging" ? "active" : ''} as={Link} to='/postagging'>POS Tagging
            </Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </div>
  );
};
export default NavBar;