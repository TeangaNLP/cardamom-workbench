import React, { useState } from "react";
import axios from "axios";
import "./FileUpload.css";
import { NavBar } from "../../components";

export default function FileUpload({ user, setUser }) {
  const [selectedFile, setSelectedFile] = useState();
  const [selectedLang, setLang] = useState("ga");
  const [status, setStatus] = useState("");


  const options = [
    { value: "af", label: "Afrikaans" },
    { value: "akk", label: "Akkadian" },
    { value: "aqz", label: "Akuntsu" },
    { value: "sq", label: "Albanian" },
    { value: "am", label: "Amharic" },
    { value: "grc", label: "Ancient Greek" },
    { value: "hbo", label: "Ancient Hebrew" },
    { value: "apu", label: "Apurina" },
    { value: "ar", label: "Arabic" },
    { value: "hy", label: "Armenian" },
    { value: "aii", label: "Assyrian" },
    { value: "bm", label: "Bambara" },
    { value: "eu", label: "Basque" },
    { value: "bej", label: "Beja" },
    { value: "be", label: "Belarusian" },
    { value: "bn", label: "Bengali" },
    { value: "bho", label: "Bhojpuri" },
    { value: "br", label: "Breton" },
    { value: "bg", label: "Bulgarian" },
    { value: "bxr", label: "Buryat" },
    { value: "yue", label: "Cantonese" },
    { value: "ca", label: "Catalan" },
    { value: "ceb", label: "Cebuano" },
    { value: "zh", label: "Chinese" },
    { value: "ckt", label: "Chukchi" },
    { value: "lzh", label: "Classical Chinese" },
    { value: "cop", label: "Coptic" },
    { value: "hr", label: "Croatian" },
    { value: "cs", label: "Czech" },
    { value: "da", label: "Danish" },
    { value: "nl", label: "Dutch" },
    { value: "en", label: "English" },
    { value: "myv", label: "Erzya" },
    { value: "et", label: "Estonian" },
    { value: "fo", label: "Faroese" },
    { value: "fi", label: "Finnish" },
    { value: "fr", label: "French" },
    { value: "qfn", label: "Frisian Dutch" },
    { value: "gl", label: "Galician" },
    { value: "de", label: "German" },
    { value: "got", label: "Gothic" },
    { value: "el", label: "Greek" },
    { value: "gub", label: "Guajajara" },
    { value: "gn", label: "Guarani" },
    { value: "he", label: "Hebrew" },
    { value: "hi", label: "Hindi" },
    { value: "qhe", label: "Hindi English" },
    { value: "hit", label: "Hittite" },
    { value: "hu", label: "Hungarian" },
    { value: "is", label: "Icelandic" },
    { value: "id", label: "Indonesian" },
    { value: "ga", label: "Irish" },
    { value: "it", label: "Italian" },
    { value: "ja", label: "Japanese" },
    { value: "jv", label: "Javanese" },
    { value: "urb", label: "Kaapor" },
    { value: "xnr", label: "Kangri" },
    { value: "krl", label: "Karelian" },
    { value: "arr", label: "Karo" },
    { value: "kk", label: "Kazakh" },
    { value: "kfm", label: "Khunsari" },
    { value: "quc", label: "Kiche" },
    { value: "koi", label: "Komi Permyak" },
    { value: "kpv", label: "Komi Zyrian" },
    { value: "ko", label: "Korean" },
    { value: "kmr", label: "Kurmanji" },
    { value: "la", label: "Latin" },
    { value: "lv", label: "Latvian" },
    { value: "lij", label: "Ligurian" },
    { value: "lt", label: "Lithuanian" },
    { value: "olo", label: "Livvi" },
    { value: "nds", label: "Low Saxon" },
    { value: "jaa", label: "Madi" },
    { value: "mpu", label: "Makurap" },
    { value: "mt", label: "Maltese" },
    { value: "gv", label: "Manx" },
    { value: "mr", label: "Marathi" },
    { value: "gun", label: "Mbya Guarani" },
    { value: "mdf", label: "Moksha" },
    { value: "myu", label: "Munduruku" },
    { value: "pcm", label: "Naija" },
    { value: "nyq", label: "Nayini" },
    { value: "nap", label: "Neapolitan" },
    { value: "sme", label: "North Sami" },
    { value: "no", label: "Norwegian" },
    { value: "cu", label: "Old Church Slavonic" },
    { value: "orv", label: "Old East Slavic" },
    { value: "fro", label: "Old French" },
    { value: "sga", label: "Old Irish" },
    { value: "otk", label: "Old Turkish" },
    { value: "fa", label: "Persian" },
    { value: "pl", label: "Polish" },
    { value: "qpm", label: "Pomak" },
    { value: "pt", label: "Portuguese" },
    { value: "ro", label: "Romanian" },
    { value: "ru", label: "Russian" },
    { value: "sa", label: "Sanskrit" },
    { value: "gd", label: "Scottish Gaelic" },
    { value: "sr", label: "Serbian" },
    { value: "sms", label: "Skolt Sami" },
    { value: "sk", label: "Slovak" },
    { value: "sl", label: "Slovenian" },
    { value: "soj", label: "Soi" },
    { value: "ajp", label: "South Levantine Arabic" },
    { value: "es", label: "Spanish" },
    { value: "sv", label: "Swedish" },
    { value: "swl", label: "Swedish Sign Language" },
    { value: "gsw", label: "Swiss German" },
    { value: "tl", label: "Tagalog" },
    { value: "ta", label: "Tamil" },
    { value: "tt", label: "Tatar" },
    { value: "eme", label: "Teko" },
    { value: "te", label: "Telugu" },
    { value: "th", label: "Thai" },
    { value: "tpn", label: "Tupinamba" },
    { value: "tr", label: "Turkish" },
    { value: "qtd", label: "Turkish German" },
    { value: "uk", label: "Ukrainian" },
    { value: "xum", label: "Umbrian" },
    { value: "hsb", label: "Upper Sorbian" },
    { value: "ur", label: "Urdu" },
    { value: "ug", label: "Uyghur" },
    { value: "vi", label: "Vietnamese" },
    { value: "wbp", label: "Warlpiri" },
    { value: "cy", label: "Welsh" },
    { value: "hyw", label: "Western Armenian" },
    { value: "wo", label: "Wolof" },
    { value: "sjo", label: "Xibe" },
    { value: "sah", label: "Yakut" },
    { value: "yo", label: "Yoruba" },
    { value: "ess", label: "Yupik" },
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
    const file_upload_url = process.env.REACT_APP_PORT ? `http://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/fileUpload` 
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
