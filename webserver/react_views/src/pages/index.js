import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import { Tagging } from "./Tagging";
import { FileUpload } from "./FileUpload";

const Pages = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<FileUpload />} />
        <Route exact path="/tagging" element={<Tagging />} />
      </Routes>
    </BrowserRouter>
  );
};
export default Pages;
