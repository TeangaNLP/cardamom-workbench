import { useLocation } from 'react-router-dom';
import { Navbar, Container, Nav } from 'react-bootstrap';

import 'bootstrap/dist/css/bootstrap.css';

const NavBar = () => {

  const location = useLocation();

  return (
    <div>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand >Cardamom Workbench</Navbar.Brand>
          <Nav activeKey={location.pathname} className="me-auto">
            <Nav.Link href="/">Home
            </Nav.Link>
            <Nav.Link href="/fileupload">File Upload
            </Nav.Link>
            <Nav.Link href="/tokeniser">Tokenisation
            </Nav.Link>
            <Nav.Link href="/postagging">POS Tagging
            </Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </div>
  );
};
export default NavBar;