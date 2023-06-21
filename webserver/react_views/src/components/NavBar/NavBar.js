import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Navbar, Container, Nav } from 'react-bootstrap';
import globalContext from '../../routes/Router';


import 'bootstrap/dist/css/bootstrap.css';
import "./NavBar.css";

const NavBar = ({ pages, setUser, main = true }) => {
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
              return <Nav.Link style={{color: activeLink == path ? "red" : "white" }}  as={Link} to={path}>{name}
              </Nav.Link>
            })}
	  { main 
		? <Nav.Link 
	      style={{color: "white" }}
	      as={Link} to={"/login"}
	      onClick={()=> {setUser(null);localStorage.removeItem("user");location.reload()}}
	      >Logout </Nav.Link>
	        : '' }
          </Nav> 
        </Container>
      </Navbar>
    </div>
  );
};
export default NavBar;
