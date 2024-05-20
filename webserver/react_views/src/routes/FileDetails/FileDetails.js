import axios from "axios";
import "./FileDetails.css";
import { NavBar } from "../../components";
import {
  AppBar,
  Box,
  Button,
  Divider,
  IconButton,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  ThemeProvider,
  Toolbar,
  Typography,
  createTheme,
} from "@mui/material";
import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Link, Outlet, useNavigate, useParams } from "react-router-dom";
import InboxIcon from "@mui/icons-material/Inbox";
import DraftsIcon from "@mui/icons-material/Drafts";
import SideNavBar from "../../components/SideNavBar/SideNavBar";
import { ArrowBack as ArrowBackIcon } from "@mui/icons-material";

const FileDetails = ({ user }) => {
  const { fileId } = useParams();
  const [fileInfo, setFileInfo] = React.useState("");

  const getAll = () => {
    const file_Info = user.documents.find((e) => e.file_id == fileId);
    setFileInfo(file_Info);
  };
  React.useEffect(() => {
    getAll();
  }, []);

  return (
    <div>
      <NavBar />
      <SideNavBar />
      <Box
        sx={{
          marginTop: "132px",
          padding: "15px 25px 15px 0px",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <AppBar
          position="fixed"
          sx={{
            marginTop: "128px",
            marginLeft: "500px",
            left: "unset",
            right: "unset",
          }}
        >
          <Toolbar>
            <Link to="/files">
              {" "}
              <IconButton edge="start" color="inherit" aria-label="menu">
                <ArrowBackIcon sx={{ color: "#fff" }} />
              </IconButton>
            </Link>
            <Typography variant="h6" component="div">
              {fileInfo?.filename}
            </Typography>
          </Toolbar>
        </AppBar>
        <Outlet
          sx={
            {
              // zIndex: (theme) => theme.zIndex.drawer + 1,
              // backgroundColor: "transparent",
              // color: "black",
            }
          }
        />
      </Box>
    </div>
  );
};

export default FileDetails;
