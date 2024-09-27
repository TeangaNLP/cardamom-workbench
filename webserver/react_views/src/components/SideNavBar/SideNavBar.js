import React from "react";
import { useLocation, Link, useParams } from "react-router-dom";
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
import SplitscreenIcon from "@mui/icons-material/Splitscreen";
import CalendarViewMonthIcon from "@mui/icons-material/CalendarViewMonth";
import EditNoteIcon from "@mui/icons-material/EditNote";
import CenterFocusWeakIcon from "@mui/icons-material/CenterFocusWeak";
import { useTheme } from "@mui/material/styles";

const SideNavBar = ({}) => {
  const location = useLocation();
  const activeLink = location.pathname;
  const { fileId } = useParams();
  const theme = useTheme();

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
  console.log("fileId", fileId);
  const pages = [
    { path: `/files/${fileId}/text-editor`, name: "Text Editor" },
    { path: `/files/${fileId}/tokeniser`, name: "Tokenisation" },
    { path: `/files/${fileId}/identification`, name: "Identification" },
    { path: `/files/${fileId}/annotation`, name: "Annotation" },
  ];
  return (
    <>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <Box sx={{ display: "flex" }}>
          <Drawer
            variant="permanent"
            sx={{
              width: 195,
              flexShrink: 0,
              [`& .MuiDrawer-paper`]: {
                width: 195,
                boxSizing: "border-box",
                // backgroundColor: darkTheme.palette.background.paper,
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
                    SplitscreenIcon,
                    CenterFocusWeakIcon,
                    EditNoteIcon,
                    ,
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
                            color:
                              activeLink === page.path
                                ? theme.palette.primary.main
                                : "inherit",
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
        </Box>
      </ThemeProvider>
    </>
  );
};

export default SideNavBar;
