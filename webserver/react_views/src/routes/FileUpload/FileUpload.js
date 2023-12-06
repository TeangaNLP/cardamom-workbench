import React, { useState } from "react";
import axios from "axios";
import "./FileUpload.css";
import { NavBar } from "../../components";

export default function FileUpload({ user, setUser }) {
  const [selectedFile, setSelectedFile] = useState();
  const [selectedLang, setLang] = useState("ga");
  const [status, setStatus] = useState("");
  const [options, setOptions] = useState([]);
  const r = () => {
      const userId = user.id;
      const get_langs_url = process.env.REACT_APP_PORT ? `http://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/get_valid_languages/`
              :  `https://${process.env.REACT_APP_HOST}/api/get_valid_languages/`
      axios
      .get(get_files_url)
      .then(function (response) {
	    const options = response.data.lang_list
        setOptions(options.map(
	    (option) => {
	        value: option[0],
	        label: option[1]
	    }));
      })
      .catch(function (err) {
        console.log(err);
      }); }

    useEffect(() => {
	    r()
    },[])

  /*const options = [
{ value: "abq", label:"Abaza"},
{ value: "af", label:"Afrikaans"},
{ value: "aii", label:"Assyrian"},
{ value: "ajp", label:"South Levantine Arabic"},
{ value: "akk", label:"Akkadian"},
{ value: "aln", label:"Gheg"},
{ value: "am", label:"Amharic"},
{ value: "apu", label:"Apurina"},
{ value: "aqz", label:"Akuntsu"},
{ value: "ar", label:"Arabic"},
{ value: "arr", label:"Karo"},
{ value: "azz", label:"Highland Puebla Nahuatl"},
{ value: "be", label:"Belarusian"},
{ value: "bej", label:"Beja"},
{ value: "bg", label:"Bulgarian"},
{ value: "bho", label:"Bhojpuri"},
{ value: "bm", label:"Bambara"},
{ value: "bn", label:"Bengali"},
{ value: "bor", label:"Bororo"},
{ value: "br", label:"Breton"},
{ value: "bxr", label:"Buryat"},
{ value: "ca", label:"Catalan"},
{ value: "ceb", label:"Cebuano"},
{ value: "ckt", label:"Chukchi"},
{ value: "cop", label:"Coptic"},
{ value: "cs", label:"Czech"},
{ value: "cu", label:"Old Church Slavonic"},
{ value: "cy", label:"Welsh"},
{ value: "da", label:"Danish"},
{ value: "de", label:"German"},
{ value: "el", label:"Greek"},
{ value: "eme", label:"Teko"},
{ value: "en", label:"English"},
{ value: "es", label:"Spanish"},
{ value: "ess", label:"Yupik"},
{ value: "et", label:"Estonian"},
{ value: "eu", label:"Basque"},
{ value: "fa", label:"Persian"},
{ value: "fi", label:"Finnish"},
{ value: "fo", label:"Faroese"},
{ value: "fr", label:"French"},
{ value: "frm", label:"Middle French"},
{ value: "fro", label:"Old French"},
{ value: "ga", label:"Irish"},
{ value: "gd", label:"Scottish Gaelic"},
{ value: "gl", label:"Galician"},
{ value: "gn", label:"Guarani"},
{ value: "got", label:"Gothic"},
{ value: "grc", label:"Ancient Greek"},
{ value: "gsw", label:"Swiss German"},
{ value: "gub", label:"Guajajara"},
{ value: "gun", label:"Mbya Guarani"},
{ value: "gv", label:"Manx"},
{ value: "hbo", label:"Ancient Hebrew"},
{ value: "he", label:"Hebrew"},
{ value: "hi", label:"Hindi"},
{ value: "hit", label:"Hittite"},
{ value: "hr", label:"Croatian"},
{ value: "hsb", label:"Upper Sorbian"},
{ value: "ht", label:"Haitian Creole"},
{ value: "hu", label:"Hungarian"},
{ value: "hy", label:"Armenian"},
{ value: "hyw", label:"Western Armenian"},
{ value: "id", label:"Indonesian"},
{ value: "is", label:"Icelandic"},
{ value: "it", label:"Italian"},
{ value: "ja", label:"Japanese"},
{ value: "jaa", label:"Madi"},
{ value: "jv", label:"Javanese"},
{ value: "ka", label:"Georgian"},
{ value: "kfm", label:"Khunsari"},
{ value: "kk", label:"Kazakh"},
{ value: "kmr", label:"Kurmanji"},
{ value: "ko", label:"Korean"},
{ value: "koi", label:"Komi Permyak"},
{ value: "kpv", label:"Komi Zyrian"},
{ value: "krl", label:"Karelian"},
{ value: "ky", label:"Kyrgyz"},
{ value: "la", label:"Latin"},
{ value: "lij", label:"Ligurian"},
{ value: "lt", label:"Lithuanian"},
{ value: "lv", label:"Latvian"},
{ value: "lzh", label:"Classical Chinese"},
{ value: "mdf", label:"Moksha"},
{ value: "mk", label:"Macedonian"},
{ value: "ml", label:"Malayalam"},
{ value: "mpu", label:"Makurap"},
{ value: "mr", label:"Marathi"},
{ value: "mt", label:"Maltese"},
{ value: "myu", label:"Munduruku"},
{ value: "myv", label:"Erzya"},
{ value: "nap", label:"Neapolitan"},
{ value: "nds", label:"Low Saxon"},
{ value: "nhi", label:"Western Sierra Puebla Nahuatl"},
{ value: "nl", label:"Dutch"},
{ value: "no", label:"Norwegian"},
{ value: "nyq", label:"Nayini"},
{ value: "olo", label:"Livvi"},
{ value: "orv", label:"Old East Slavic"},
{ value: "otk", label:"Old Turkish"},
{ value: "pcm", label:"Naija"},
{ value: "pl", label:"Polish"},
{ value: "pt", label:"Portuguese"},
{ value: "qaf", label:"Maghrebi Arabic French"},
{ value: "qfn", label:"Frisian Dutch"},
{ value: "qpm", label:"Pomak"},
{ value: "qtd", label:"Turkish German"},
{ value: "quc", label:"Kiche"},
{ value: "ro", label:"Romanian"},
{ value: "ru", label:"Russian"},
{ value: "sa", label:"Sanskrit"},
{ value: "sah", label:"Yakut"},
{ value: "say", label:"Zaar"},
{ value: "sga", label:"Old Irish"},
{ value: "si", label:"Sinhala"},
{ value: "sjo", label:"Xibe"},
{ value: "sk", label:"Slovak"},
{ value: "sl", label:"Slovenian"},
{ value: "sme", label:"North Sami"},
{ value: "sms", label:"Skolt Sami"},
{ value: "soj", label:"Soi"},
{ value: "sq", label:"Albanian"},
{ value: "sr", label:"Serbian"},
{ value: "sv", label:"Swedish"},
{ value: "swl", label:"Swedish Sign Language"},
{ value: "ta", label:"Tamil"},
{ value: "te", label:"Telugu"},
{ value: "th", label:"Thai"},
{ value: "tl", label:"Tagalog"},
{ value: "tpn", label:"Tupinamba"},
{ value: "tr", label:"Turkish"},
{ value: "tt", label:"Tatar"},
{ value: "ug", label:"Uyghur"},
{ value: "uk", label:"Ukrainian"},
{ value: "ur", label:"Urdu"},
{ value: "urb", label:"Kaapor"},
{ value: "vep", label:"Veps"},
{ value: "vi", label:"Vietnamese"},
{ value: "wbp", label:"Warlpiri"},
{ value: "wo", label:"Wolof"},
{ value: "xav", label:"Xavante"},
{ value: "xcl", label:"Classical Armenian"},
{ value: "xnr", label:"Kangri"},
{ value: "xum", label:"Umbrian"},
{ value: "yo", label:"Yoruba"},
{ value: "yrl", label:"Nheengatu"},
{ value: "yue", label:"Cantonese"},
{ value: "zh", label:"Chinese"},
  ];*/


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
