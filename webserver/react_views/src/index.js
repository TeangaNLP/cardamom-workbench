import { render } from "react-dom";
import React from 'react';
import { BrowserRouter, 
         Routes,
         Route,
       } from "react-router-dom";
import Home from "./routes/home";
import POSTagging from "./routes/pos_tagging";   

const rootElement = document.getElementById("root");

render(
  <BrowserRouter>
    <Routes>
        <Route path="/"  element={<Home />} /> 
        <Route path="/postagging" element={<POSTagging />} />
    </Routes>
  </BrowserRouter>,
  rootElement
);
