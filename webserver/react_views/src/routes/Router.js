import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Login } from "./Login/";
import { Home } from "./Home/";
import { FileUpload } from "./FileUpload/";
import { Tagging } from "./Tagging";
import { Tokeniser } from "./Tokeniser";
import { useEffect, useState } from "react";


export default function Router() {
  const [userId, setUserId] = useState();
  const [fileInfo, setFileInfo] = useState({});

  console.log("In router", userId);

  useEffect(() => {
    console.log('Mounted');
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login setUserId={setUserId} />} />
        <Route path="/" element={<Home setFileInfo={setFileInfo} userId={userId} />} />
        <Route path="/fileupload" element={<FileUpload userId={userId} />} />
        <Route path="/tokeniser" element={<Tokeniser fileInfo={fileInfo} userId={userId} />} />
        <Route path="/tagging" element={<Tagging fileInfo={fileInfo} userId={userId} />} />
        <Route path="/editor" element={<Tagging fileInfo={fileInfo} userId={userId} />} />
        <Route path="/identification" element={<Tagging fileInfo={fileInfo} userId={userId} />} />
        <Route path="/annotation" element={<Tagging fileInfo={fileInfo} userId={userId} />} />
      </Routes>
    </BrowserRouter>
  );
}
