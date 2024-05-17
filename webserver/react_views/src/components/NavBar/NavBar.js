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
import { AccountCircle } from "@mui/icons-material";
import { Avatar } from "rsuite";

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
    localStorage.removeItem("user");
    location.reload();
  };

  return (
    <AppBar position="static" color={main ? "primary" : "secondary"}>
      <Toolbar>
        {main && (
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Cardamom Workbench
          </Typography>
        )}
        <Box sx={{ flexGrow: 1 }}>
          {pages.map((page) => (
            <Button
              key={page.path}
              component={Link}
              to={page.path}
              sx={{ color: activeLink === page.path ? "red" : "white" }}
            >
              {page.name}
            </Button>
          ))}
        </Box>
        {main && (
          <div>
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
