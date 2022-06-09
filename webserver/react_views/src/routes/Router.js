import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Login } from "./Login/";
import { Home } from "./Home/";
import { FileUpload } from "./FileUpload/";
import { PosTagging } from "./PosTagging";
import { Tokeniser } from "./Tokeniser";
import { useEffect, useState } from "react";


export default function Router() {
  const [userId, setUserId] = useState();

  console.log("In router", userId);

  useEffect(() => {
    console.log('Mounted');
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login setUserId={setUserId} />} />
        <Route path="/" element={<Home userId={userId} />} />
        <Route path="/fileupload" element={<FileUpload userId={userId} />} />
        <Route path="/tokeniser" element={<Tokeniser userId={userId} />} />
        <Route path="/postagging" element={<PosTagging userId={userId} />} />
      </Routes>
    </BrowserRouter>
  );
}
