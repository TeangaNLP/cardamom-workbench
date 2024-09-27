import React, { useState, useEffect } from "react";
import { useLocation, Link, useParams } from "react-router-dom";
import axios from "axios";
import {
  Drawer,
  List,
  ListItem,
  ListItemText,
  Button,
  CircularProgress,
  Box,
  Snackbar,
  Alert,
} from "@mui/material";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css"; // Import Quill's snow theme CSS
import "./TextEditor.css";

const TextEditor = ({ user }) => {
  const location = useLocation();
  const [content, setContent] = useState("");
  const [counter, setCounter] = useState(0);
  const [saveSuccess, setSaveSuccess] = useState(false); // New state for save success

  const [documentsList, setDocuments] = useState([]);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

  const [isLoading, setIsLoading] = useState(true);
  const { fileId } = useParams();
  const [changedItems, setChangedItems] = useState([]);
  const [isSaving, setIsSaving] = useState(false);

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
        const doc = documents.find((e) => (e.filename == fileId) !== undefined);
        console.log("doc", doc);
        setContent(doc.content);
        setDocuments(documents);
        setIsLoading(false);
        // set(documents);
        console.log(documents);
      })
      .catch(function (err) {
        console.log(err);
      });
  };

  useEffect(() => {
    if (!documentsList.length) {
      getAll();
    }
  }, []);
  const handleChange = (value) => {
    setCounter(counter + 1);
    setContent(value);
    console.log("handleChange", value);
    if (counter > 2) {
      console.log("trigger state update");
      setHasUnsavedChanges(true); // Set unsaved changes flag
    }
  };
  // Handle save action
  const handleSave = async () => {
    setIsSaving(true);
    setHasUnsavedChanges(false); // Reset unsaved changes flag

    // Simulate an API call or asynchronous operation
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setIsSaving(false);
    setHasUnsavedChanges(false); // Reset unsaved changes flag
    setSaveSuccess(true); // Set save success flag
    setTimeout(() => setSaveSuccess(false), 3000);
  };
  // useEffect(() => {
  //   // Listen for beforeunload event to show a warning when the user tries to leave the page with unsaved changes
  //   const handleBeforeUnload = (event) => {
  //     if (hasUnsavedChanges) {
  //       event.preventDefault();
  //       event.returnValue = ""; // Required for Chrome
  //     }
  //   };

  //   window.addEventListener("beforeunload", handleBeforeUnload);

  //   return () => {
  //     window.removeEventListener("beforeunload", handleBeforeUnload);
  //   };
  // }, [hasUnsavedChanges]);
  return (
    <div
      style={{
        height: "350px",
        width: "100%",
        marginLeft: "240px",
        marginRight: "10px",
      }}
    >
      {/* <Snackbar
        open={saveSuccess}
        message="Changes saved successfully!"
        // sx={{
        //   backgroundColor: "#4caf50", // Success color
        // }}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        autoHideDuration={3000}
      /> */}

      <Snackbar
        open={saveSuccess}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        // autoHideDuration={}
      >
        <Alert
          severity="success"
          color="info"
          variant="filled"
          sx={{
            width: "100%",
            color: "#389e0d",
            background: "#f6ffed",
            borderColor: "#b7eb8f",
          }}
        >
          Saved Successfully!
        </Alert>
      </Snackbar>

      <Snackbar
        open={hasUnsavedChanges}
        message="You have unsaved changes."
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        autoHideDuration={3000}
      />
      <ReactQuill
        theme="snow"
        value={content}
        onChange={handleChange}
        placeholder="Start typing..."
        style={{ height: "100%" }}
      />
      <Box
        sx={{
          marginTop: "80px",
          float: "right",
          // position: "absolute",
          // bottom: "16px",
          // right: "16px",
          // marginTop: "16px", // Add margin-top to create separation
        }}
      >
        <Button
          variant="contained"
          color="primary"
          onClick={handleSave}
          size="large" // Increase size of the button
          disabled={isSaving}
          startIcon={isSaving && <CircularProgress size={24} />}
        >
          {isSaving ? "Saving..." : "Save"}
        </Button>
      </Box>
    </div>
  );
};

export default TextEditor;
