import { useLocation, Link } from 'react-router-dom';
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
            <Nav.Link as={Link} to = '/'>Home
            </Nav.Link>
            <Nav.Link as={Link} to = '/fileupload'>File Upload
            </Nav.Link>
            <Nav.Link as={Link} to = '/tokeniser' >Tokenisation
            </Nav.Link>
            <Nav.Link as={Link} to = '/postagging'>POS Tagging
            </Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </div>
  );
};
export default NavBar;