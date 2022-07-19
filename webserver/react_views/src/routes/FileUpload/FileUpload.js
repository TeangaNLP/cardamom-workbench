import React, { useState } from "react";
import axios from "axios";
import "./FileUpload.css";
import { NavBar } from "../../components";

export default function FileUpload(props) {
  const [selectedFile, setSelectedFile] = useState();

  const userId = props.userId;

  const changeHandler = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmission = () => {
    const data = new FormData();
    data.append("file", selectedFile);
    data.append("user_id", userId);
    axios
      .post("http://localhost:5001/api/fileUpload", data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then(function (response) {
        console.log("Successfully uploaded!");
      })
      .catch(function () {
        console.log("Didn't upload");
      });
  };

  return (
    <div>
      <NavBar pages={[{ path: "/", name: "Home" }, { path: "/fileupload", name: "File Upload" }]} />
      <br />
      <h2> Cardamom Workbench</h2>
      <div id="file-upload-form" className="uploader">
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
      </div>
    </div>
  );
}
