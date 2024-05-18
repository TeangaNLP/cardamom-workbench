import React from "react";
import { useLocation, Link } from "react-router-dom";
import {
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Toolbar,
  Box,
  CssBaseline,
} from "@mui/material";
import {
  InsertDriveFile as InsertDriveFileIcon,
  Edit as EditIcon,
  Token as TokenIcon,
  Face as FaceIcon,
  Label as LabelIcon,
} from "@mui/icons-material";
import { ThemeProvider, createTheme } from "@mui/material/styles";

const SideNavBar = ({}) => {
  const location = useLocation();
  const activeLink = location.pathname;
  const darkTheme = createTheme({
    palette: {
      mode: "light",
      background: {
        // paper: "#424242",
      },
      text: {
        // primary: "#ffffff",
      },
    },
  });

  const pages = [
    { path: "/editor", name: "Text Editor" },
    // { path: `/tokeniser/${fileInfo.file_id}`, name: "Tokenisation" },
    { path: "/identification", name: "Identification" },
    { path: "/annotation", name: "Annotation" },
    { path: activeLink, name: "POS Tagging" },
  ];

  return (
    <>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <Drawer
          variant="permanent"
          sx={{
            width: 195,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: {
              width: 195,
              boxSizing: "border-box",
              backgroundColor: darkTheme.palette.background.paper,
              color: darkTheme.palette.text.primary,
            },
          }}
        >
          <Toolbar>
            {/* <Box
              component="img"
              src={`${process.env.PUBLIC_URL}/cardamom-transparent.png`}
              alt="Logo"
              sx={{ width: "190px", height: "auto", mb: 2, mt: 2 }}
            /> */}
          </Toolbar>
          <Box sx={{ overflow: "auto", mb: 3, mt: 3 }}>
            <List>
              {pages.map((page, index) => {
                const Icon = [
                  EditIcon,
                  TokenIcon,
                  FaceIcon,
                  LabelIcon,
                  InsertDriveFileIcon,
                ][index];
                return (
                  <ListItem
                    button
                    component={Link}
                    to={page.path}
                    key={page.name}
                    selected={activeLink === page.path}
                  >
                    <ListItemIcon>
                      <Icon
                        style={{
                          color: activeLink === page.path ? "red" : "inherit",
                        }}
                      />
                    </ListItemIcon>
                    <ListItemText primary={page.name} />
                  </ListItem>
                );
              })}
            </List>
          </Box>
        </Drawer>
      </ThemeProvider>
    </>
  );
};

export default SideNavBar;
