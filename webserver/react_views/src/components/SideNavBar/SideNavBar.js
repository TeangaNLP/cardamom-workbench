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
} from "@mui/material";
import {
  InsertDriveFile as InsertDriveFileIcon,
  Edit as EditIcon,
  Token as TokenIcon,
  Face as FaceIcon,
  Label as LabelIcon,
} from "@mui/icons-material";

const SideNavBar = ({ pages }) => {
  const location = useLocation();
  const activeLink = location.pathname;

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 240,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: 240, boxSizing: "border-box" },
      }}
    >
      <Toolbar>
        <Box
          component="img"
          src={`${process.env.PUBLIC_URL}/cardamom-transparent.png`}
          alt="Logo"
          sx={{ width: "190px", height: "auto", mb: 2, mt: 2 }}
        />
      </Toolbar>

      <Box sx={{ overflow: "auto" }}>
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
  );
};

export default SideNavBar;
