import axios from "axios";
import "./FileDetails.css";
import { NavBar } from "../../components";
import {
  AppBar,
  Box,
  Divider,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Outlet, useNavigate, useParams } from "react-router-dom";
import InboxIcon from "@mui/icons-material/Inbox";
import DraftsIcon from "@mui/icons-material/Drafts";
import SideNavBar from "../../components/SideNavBar/SideNavBar";

const FileDetails = ({}) => {
  return (
    <div>
      <NavBar />
      <SideNavBar />
      <Box
        sx={{
          marginTop: "64px",
          padding: "25px",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Outlet />
      </Box>
    </div>
  );
};

export default FileDetails;
