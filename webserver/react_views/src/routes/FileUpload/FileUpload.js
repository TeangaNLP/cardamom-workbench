import React, { useState } from "react";
import axios from "axios";
import "./FileUpload.css";
import { NavBar } from "../../components";

export default function FileUpload({ user, setUser }) {
  const [selectedFile, setSelectedFile] = useState();
  const [selectedLang, setLang] = useState("ga");
  const [status, setStatus] = useState("");


  const options = [
    { value: "ga", label: "Irish" },
    { value: "en", label: "English" },
    { value: "sga", label: "Old Irish" },
  ];


  const changeHandler = (event) => {
    setStatus("")
    setSelectedFile(event.target.files[0]);
  };

  const changeLang = (event) => {
    setLang(event.target.value);

  }

  const handleSubmission = () => {
    const userId = user.id;
    const data = new FormData();
    data.append("file", selectedFile);
    data.append("user_id", userId);
    data.append("iso_code", selectedLang)
    const file_upload_url = process.env.REACT_APP_PORT ? `https://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/fileUpload` 
		  :  `https://${process.env.REACT_APP_HOST}/api/fileUpload` 
     
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
      <br />
      <h2> Cardamom Workbench</h2>
      <h2 style={{ color: 'red' }}> {status} </h2>

      <div id="file-upload-form" className="uploader">
        <select
          options={options}
          onChange={changeLang}
        >
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
      </div>
    </div>
  );
}
