import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Navbar, Container, Nav } from 'react-bootstrap';


import 'bootstrap/dist/css/bootstrap.css';
import "./NavBar.css";

const NavBar = ({ pages, main = true }) => {
  const location = useLocation();
  const activeLink = location.pathname;

  return (
    <div>
      <Navbar bg={main ? "dark" : null} className={main ? null : "secondary-bar"} variant="dark">
        <Container>
          {main ? <Navbar.Brand >Cardamom Workbench</Navbar.Brand> : null}
          <Nav>
            {pages.map((page) => {
              const path = page.path;
              const name = page.name;
              return <Nav.Link className={activeLink == path ? "active" : ''} as={Link} to={path}>{name}
              </Nav.Link>
            })}
          </Nav>
        </Container>
      </Navbar>
    </div>
  );
};
export default NavBar;