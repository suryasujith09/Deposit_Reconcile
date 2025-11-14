import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { FaUpload } from "react-icons/fa";

function UploadForm({ setResultData }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      toast.error("Please select an image file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoading(true);
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResultData(response.data);
      toast.success("Analysis completed successfully!");
    } catch (error) {
      console.error(error);
      toast.error("Error analyzing the slip. Check backend logs!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card upload-card shadow-sm p-4 text-center">
      <h5 className="mb-3">Upload Bank Deposit Slip</h5>

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <input
            type="file"
            accept="image/*"
            className="form-control"
            onChange={handleFileChange}
          />
        </div>

        <button
          className="btn btn-primary w-100"
          type="submit"
          disabled={loading}
        >
          {loading ? "Processing..." : <><FaUpload /> Upload & Analyze</>}
        </button>
      </form>
    </div>
  );
}

export default UploadForm;
