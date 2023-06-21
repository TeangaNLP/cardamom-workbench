import { useState, useContext, createContext } from "react";
import { BrowserRouter, Routes, Route, useNavigate, useLocation } from "react-router-dom";
import { Login } from "./Login/";
import  SignUp  from "./SignUp/SignUp";
import { Home } from "./Home/";
import { FileUpload } from "./FileUpload/";
import { Tagging } from "./Tagging";
import { Tokeniser } from "./Tokeniser";
import CheckCachedUser from "../components/checkCachedUser";
import RequireUser from "../components/requireUser";
import RequireFileInfo from "../components/requireFileInfo";


export const appContext = createContext({
	user: null,
	fileInfo: null,
	documents: null,
	logout: () => { }
	})

export default function Router() {
  const [userId, setUserId] = useState();
  const [user, setUser] = useState();
  const [fileInfo, setFileInfo] = useState(null);
  const [documents, setDocuments] = useState(null);
  const logout = () => {
	setFileInfo(null)
	setDocuments(null)
	setUser(null)
	localStorage.removeItem("user")
  }

  return (
    <BrowserRouter>
      <appContext.Provider value={{
		user, fileInfo, documents, logout
      }}>
      <Routes>
        <Route path="/login" element={
		<CheckCachedUser user={user} setUser={setUser} redirectTo="/">
			<Login setUser={setUser} setUserId={setUserId} /> 
		</CheckCachedUser>
		} 
	/>
        <Route path="/signup" element={
			<SignUp setUser={setUser} setUserId={setUserId} /> 
		} 
	/>
        <Route path="/" element={
		<RequireUser user={user} setUser={setUser} redirectTo="/login" >
			<Home user={user} setUser={setUser}
			      documents={documents} setDocuments={setDocuments}
			      setFileInfo={setFileInfo} />
		</RequireUser>
		} 
	/>
        <Route path="/fileupload" element={
			<RequireUser user={user} setUser={setUser} redirectTo="/login" >
					<FileUpload setUser={setUser} user={user} />
			</RequireUser>
					}
	/>
        <Route path="/tokeniser/:fileId" element={
		<RequireUser user={user} setUser={setUser} redirectTo="/login" >
			<RequireFileInfo user={user} setUser={setUser}
					fileInfo={fileInfo} setFileInfo={setFileInfo} redirectTo="/login" >
				<Tokeniser  fileInfo={fileInfo} setFileInfo={setFileInfo}
					    user={user} setUser={setUser} />
			</RequireFileInfo>
		</RequireUser>
		} 
	 />
        <Route path="/tagging/:fileId" element={
		<RequireUser user={user} setUser={setUser} redirectTo="/login" >
			<RequireFileInfo user={user} setUser={setUser}
					fileInfo={fileInfo} setFileInfo={setFileInfo} redirectTo="/login" >
				<Tagging setUser={setUser} fileInfo={fileInfo} user={user} />
			</RequireFileInfo>
		</RequireUser>
			} 
	/>
      </Routes>
     </ appContext.Provider> 
    </BrowserRouter>
  );
}
