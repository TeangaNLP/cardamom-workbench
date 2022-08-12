import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Login } from "./Login/";
import { Home } from "./Home/";
import { FileUpload } from "./FileUpload/";
import { Tagging } from "./Tagging";
import { Tokeniser } from "./Tokeniser";
import { useEffect, useState } from "react";


export default function Router() {
  const [userId, setUserId] = useState();
  /*
   fileinfo =  {
           file_id: file_id,
            content: content,
            lang_id: lang_id
    }
   */
  const [fileInfo, setFileInfo] = useState({});
  const [documents, setDocuments] = useState([]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login setUserId={setUserId} />} />
        <Route path="/" element={<Home userId={userId}
          documents={documents} setDocuments={setDocuments}
          setFileInfo={setFileInfo} />} />
        <Route path="/fileupload" element={<FileUpload userId={userId} />} />
        <Route path="/tokeniser" element={<Tokeniser fileInfo={fileInfo} setFileInfo={setFileInfo}
          userId={userId} />} />
        <Route path="/tagging" element={<Tagging fileInfo={fileInfo} userId={userId} />} />
      </Routes>
    </BrowserRouter>
  );
}
