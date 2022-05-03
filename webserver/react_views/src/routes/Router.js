import React from 'react';
import { BrowserRouter, 
         Routes,
         Route,
       } from "react-router-dom";
import Home from "./Home/Home";
import PosTagging from "./PosTagging/PosTagging";   

export default function Router(){ 
  return (
  <BrowserRouter>
    <Routes>
        <Route path="/"  element={<Home />} /> 
        <Route path="/postagging" element={<PosTagging />} />
    </Routes>
  </BrowserRouter>
  )
}
