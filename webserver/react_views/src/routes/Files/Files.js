import axios from "axios";
import "./Files.css";
import { NavBar } from "../../components";
import {
  AppBar,
  Box,
  Button,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Navigate, Outlet } from "react-router-dom";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { styled } from "@mui/material/styles";

import { tableCellClasses } from "@mui/material/TableCell";

export default function Files({ user }) {
  const [documentsList, setDocuments] = React.useState([]);
  const navigate = useNavigate();

  const handleAction = (file) => {
    console.log("got file", file);
    navigate(`/files/${file.file_id}/text-editor`); // Replace `/details` with your desired route
  };
  const [isLoading, setIsLoading] = React.useState(true);
  const getAll = () => {
    const userId = user.id;
    const get_files_url = process.env.REACT_APP_PORT
      ? `http://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/get_files?user=` +
        userId
      : `https://${process.env.REACT_APP_HOST}/api/get_files?user=` + userId;
    axios
      .get(get_files_url)
      .then(function (response) {
        const documents = response.data.file_contents;
        setIsLoading(false);
        setDocuments(documents);
        console.log(documents);
      })
      .catch(function (err) {
        console.log(err);
      });
  };

  React.useEffect(() => {
    if (!documentsList.length) {
      getAll();
    }
  }, []);

  const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
      backgroundColor: theme.palette.primary.main,
      color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
      fontSize: 14,
    },
  }));

  const StyledTableRow = styled(TableRow)(({ theme }) => ({
    "&:nth-of-type(odd)": {
      backgroundColor: theme.palette.action.hover,
    },
    // hide last border
    "&:last-child td, &:last-child th": {
      border: 0,
    },
  }));

  return (
    <div>
      <NavBar />
      <Box
        sx={{
          marginTop: "24px",
          padding: "25px",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 700 }} aria-label="customized table">
            <TableHead>
              <TableRow>
                <StyledTableCell sx={{ width: "80px" }}>
                  File ID
                </StyledTableCell>
                <StyledTableCell align="left">File Name</StyledTableCell>
                <StyledTableCell align="left">Content</StyledTableCell>
                <StyledTableCell sx={{ width: "180px" }} align="left">
                  Action
                </StyledTableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {documentsList.map((row) => (
                <StyledTableRow key={row.file_id}>
                  <StyledTableCell component="th" scope="row">
                    {row.file_id}
                  </StyledTableCell>
                  <StyledTableCell align="left">{row.filename}</StyledTableCell>
                  <StyledTableCell align="left">
                    {" "}
                    {row.content.length > 250
                      ? row.content.slice(0, 250) + "..."
                      : row.content}
                  </StyledTableCell>
                  <StyledTableCell align="left">
                    {" "}
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => handleAction(row)}
                    >
                      View More
                    </Button>
                  </StyledTableCell>
                </StyledTableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        {/* <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>File ID</TableCell>
                <TableCell>File Name</TableCell>
                <TableCell>File Content</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {documentsList.map((item, index) => (
                <TableRow key={index}>
                  <TableCell>{item.file_id}</TableCell>
                  <TableCell>{item.filename}</TableCell>
                  <TableCell>
                    {item.content.length > 250
                      ? item.content.slice(0, 250) + "..."
                      : item.content}
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => handleAction(item)}
                    >
                      View More
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody> */}
        {/* </Table>
        </TableContainer> */}
      </Box>
    </div>
  );
}
