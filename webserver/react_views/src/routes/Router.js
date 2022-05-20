import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import { Login } from "./Login/";
import { Home } from "./Home/";
import { FileUpload } from "./FileUpload/";
import { PosTagging } from "./PosTagging";
import { Tokeniser } from './Tokeniser';

export default function Router() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Home />} />
        <Route path="/fileupload" element={<FileUpload />} />
        <Route path="/tokeniser" element={<Tokeniser />} />
        <Route path="/postagging" element={<PosTagging />} />
      </Routes>
    </BrowserRouter>
  )
}
