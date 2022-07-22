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
           fileId: fileId,
            content: location.state.content
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
