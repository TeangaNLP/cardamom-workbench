// import { useState } from 'react';
// import { Link, useLocation } from 'react-router-dom';
// import { Navbar, Container, Nav } from 'react-bootstrap';
// import globalContext from '../../routes/Router';

// import 'bootstrap/dist/css/bootstrap.css';
// import "./NavBar.css";

// const NavBar = ({ pages, setUser, main = true }) => {
//   const location = useLocation();
//   const activeLink = location.pathname;

//   return (
//     <div>
//       <Navbar bg={main ? "dark" : null} className={main ? null : "secondary-bar"} variant="dark">
//         <Container>
//           {main ? <Navbar.Brand >Cardamom Workbench</Navbar.Brand> : null}
//           <Nav>
//             {pages.map((page) => {
//               const path = page.path;
//               const name = page.name;
//               return <Nav.Link style={{color: activeLink == path ? "red" : "white" }}  as={Link} to={path}>{name}
//               </Nav.Link>
//             })}
// 	  { main
// 		? <Nav.Link
// 	      style={{color: "white" }}
// 	      as={Link} to={"/login"}
// 	      onClick={()=> {setUser(null);localStorage.removeItem("user");location.reload()}}
// 	      >Logout </Nav.Link>
// 	        : '' }
//           </Nav>
//         </Container>
//       </Navbar>
//     </div>
//   );
// };
// export default NavBar;
import React from "react";
import "./NavBar.css";
import { useLocation, Link, useNavigate } from "react-router-dom";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Box,
} from "@mui/material";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

import { AccountCircle } from "@mui/icons-material";
import { Avatar } from "rsuite";
import MenuIcon from "@mui/icons-material/Menu";
const drawerWidth = 240;
const navItems = ["Home", "About", "Contact"];
const NavBar = ({ pages, setUser, main = true, user }) => {
  const location = useLocation();
  const activeLink = location.pathname;

  const navigate = useNavigate();

  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    setUser(null);
    console.log("remove user", localStorage.getItem("user"));
    localStorage.removeItem("user");
    console.log("is it remove user", localStorage.getItem("user"));
    navigate("/login"); // Navigate to the login page

    // location.reload();
  };

  return (
    // <AppBar position="static" color={main ? "primary" : "secondary"}>
    <AppBar
      position="static"
      sx={{
        zIndex: (theme) => theme.zIndex.drawer + 1,
        backgroundColor: "transparent",
        color: "black",
      }}
    >
      <Toolbar>
        <Link className="cardamom-anchor" to="/files">
          <img
            className="cardamom-logo-appbar"
            src="../../cardamom-logo.png"
            alt="Cardamom Logo"
          />
        </Link>
        <Box sx={{ flexGrow: 1 }}>
          {/* 
          {page.map((page) => (
            <Button
              key={page.path}
              component={Link}
              to={page.path}
              sx={{ color: activeLink === page.path ? "red" : "white" }}
            >
              {page.name}
            </Button> */}
          {/* ))} */}
        </Box>
        {main && (
          <div>
            <Button color="inherit" component={Link} to="/files">
              Home
            </Button>

            <Button color="inherit" component={Link} to="/fileupload">
              Upload New Files
            </Button>
            <IconButton
              size="large"
              edge="end"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMenu}
              color="inherit"
            >
              <AccountCircle />
              {/* <Avatar sx={{ bgcolor: "primary.main", mr: 2 }}>
                {user.name.charAt(0).toUpperCase()}
              </Avatar>
              <Typography variant="body1" color="inherit">
                {user.name}
              </Typography> */}
            </IconButton>

            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </Menu>
          </div>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;
