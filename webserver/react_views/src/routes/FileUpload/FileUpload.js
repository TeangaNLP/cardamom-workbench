import React, { useState } from "react";
import axios from "axios";
import "./FileUpload.css";
import { NavBar } from "../../components";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import {
  Alert,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Snackbar,
} from "@mui/material";
import { CloudUpload, Photo } from "@mui/icons-material";

export default function FileUpload({ user, setUser }) {
  const options = [
    { value: "ga", label: "Irish" },
    { value: "en", label: "English" },
    { value: "sga", label: "Old Irish" },
  ];
  const [selectedFile, setSelectedFile] = useState();
  const [selectedLang, setLang] = useState(options[0].value);
  const [status, setStatus] = useState("");
  const [fileContent, setFileContent] = useState("");
  const [errorSuccess, setErrorSuccess] = useState(false); // New state for save success

  // const changeHandler = (event) => {
  //   setStatus("");
  //   setSelectedFile(event.target.files[0]);
  // };

  const changeHandler = (event) => {
    setSelectedFile(null);

    const file = event.target.files[0];
    if (file) {
      if (file.type === "text/plain") {
        const reader = new FileReader();
        reader.onloadend = () => {
          setFileContent(reader.result.slice(0, 200)); // Limit to first 200 characters
        };
        reader.readAsText(file);
        setSelectedFile(file);
        console.log("configured");
      } else {
        setFileContent(""); // Clear content if file type is not text
        setErrorSuccess(true);
        setTimeout(() => {
          setErrorSuccess(false);
        }, 2500);
      }
    }
  };
  const changeLang = (event) => {
    setLang(event.target.value);
  };

  const handleSubmission = () => {
    const userId = user.id;
    const data = new FormData();
    data.append("file", selectedFile);
    data.append("user_id", userId);
    data.append("iso_code", selectedLang);
    const file_upload_url = process.env.REACT_APP_PORT
      ? `http://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/fileUpload`
      : `https://${process.env.REACT_APP_HOST}/api/fileUpload`;

    axios
      .post(file_upload_url, data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then(function (response) {
        console.log("Successfully uploaded!");
        setStatus("File Successfully uploaded!");
      })
      .catch(function () {
        console.log("Didn't upload");
        setStatus("File upload failed.");
      });
  };

  return (
    <div>
      <NavBar
        setUser={setUser}
        pages={[
          { path: "/", name: "Home" },
          { path: "/fileupload", name: "File Upload" },
        ]}
      />
      <h2 style={{ color: "red" }}> {status} </h2>

      <div className="maindiv">
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Upload Files
            </Typography>
          </Toolbar>
        </AppBar>
        <Container maxWidth="md">
          {/* <div id="file-upload-form" className="uploader">
              <select options={options} onChange={changeLang}>
                {options.map((option, index) => {
                  return (
                    <option value={option.value} key={option.value}>
                      {option.label}
                    </option>
                  );
                })}
              </select>

              <label htmlFor="file-upload" id="file-drag">
                <input
                  id="file-upload"
                  type="file"
                  name="file"
                  onChange={changeHandler}
                />

                <div id="start">
                  <button
                    id="file-upload-btn"
                    className="btn btn-primary"
                    onClick={handleSubmission}
                  >
                    Submit
                  </button>
                </div>
              </label>
            </div> */}
          <Box id="file-upload-form" className="uploader" sx={{ p: 2 }}>
            <FormControl fullWidth variant="outlined" sx={{ mb: 2 }}>
              <InputLabel id="select-label">Select Option</InputLabel>
              <Select
                labelId="select-label"
                value={selectedLang}
                onChange={changeLang}
                label="Select Option"
              >
                {options.map((option) => (
                  <MenuItem value={option.value} key={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Box id="file-drag" sx={{ mb: 2 }}>
              <input
                id="file-upload"
                type="file"
                name="file"
                onChange={changeHandler}
                style={{ display: "none" }}
                accept=".txt"
              />
              <label htmlFor="file-upload">
                <Button
                  variant="contained"
                  component="span"
                  startIcon={<CloudUpload />}
                  sx={{ mr: 2 }}
                >
                  Choose File
                </Button>
              </label>
            </Box>

            {fileContent && (
              <Box
                sx={{
                  mb: 2,
                  textAlign: "left",
                  border: "1px solid #ccc",
                  padding: 2,
                  borderRadius: 1,
                }}
              >
                <Typography variant="h6">File Content:</Typography>
                <Typography
                  variant="body1"
                  component="pre"
                  sx={{ whiteSpace: "pre-wrap" }}
                >
                  {fileContent}
                </Typography>
              </Box>
            )}

            {fileContent && (
              <Box id="start" sx={{ textAlign: "center", marginTop: "16px" }}>
                <Button
                  id="file-upload-btn"
                  variant="contained"
                  color="primary"
                  onClick={handleSubmission}
                >
                  Submit
                </Button>
              </Box>
            )}
          </Box>
        </Container>
        <Snackbar
          open={errorSuccess}
          anchorOrigin={{ vertical: "top", horizontal: "center" }}
          autoHideDuration={3000}
        >
          <Alert
            severity="info"
            sx={{
              width: "100%",
              color: "#d48806",
              background: "#fffbe6",
              borderColor: "#ffe58f",
            }}
            variant="filled"
          >
            Error! Invalid User or Password
          </Alert>
        </Snackbar>
      </div>
    </div>
  );
}
