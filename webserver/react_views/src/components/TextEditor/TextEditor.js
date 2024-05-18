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

const TextEditor = ({}) => {
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

  return <div>this is a text editor x</div>;
};

export default TextEditor;
