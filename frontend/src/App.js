import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import ResultCard from "./components/ResultCard";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./App.css";

function App() {
  const [resultData, setResultData] = useState(null);

  return (
    <div className="app-container">
      <h2 className="text-center my-4 title">
        🏦 Bank Slip Analyzer
      </h2>

      <div className="upload-section">
        <UploadForm setResultData={setResultData} />
      </div>

      {resultData && (
        <div className="result-section mt-4">
          <ResultCard data={resultData} />
        </div>
      )}

      <ToastContainer position="top-center" autoClose={3000} />
    </div>
  );
}

export default App;
