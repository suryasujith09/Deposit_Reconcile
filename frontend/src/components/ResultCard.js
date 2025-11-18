import React from "react";
import { FaUser, FaRupeeSign, FaPhone, FaCalendarAlt, FaUniversity } from "react-icons/fa";

function ResultCard({ data }) {
  const fields = [
    { key: "date", label: "Date", icon: <FaCalendarAlt /> },
    { key: "branch", label: "Branch", icon: <FaUniversity /> },
    { key: "accountNumber", label: "Account No.", icon: <FaUser /> },
    { key: "name", label: "Name", icon: <FaUser /> },
    { key: "contactNumber", label: "Contact", icon: <FaPhone /> },
    { key: "amount", label: "Amount", icon: <FaRupeeSign /> },
    { key: "amountInWords", label: "Amount in Words", icon: <FaRupeeSign /> },
    { key: "chequeDetails", label: "Cheque Details", icon: <FaUniversity /> },
    // { key: "signature", label: "Signature", icon: <FaSignature /> },
  ];

  return (
    <div className="container result-container">
      <div className="card result-card shadow-lg p-4">
        <h5 className="mb-3 text-center text-primary">Extracted Information</h5>

        <div className="row">
          {fields.map(({ key, label, icon }) => (
            <div key={key} className="col-md-6 mb-3">
              <div className="info-box p-3 border rounded bg-light d-flex align-items-center">
                <span className="me-3 fs-4 text-primary">{icon}</span>
                <div>
                  <h6 className="mb-0">{label}</h6>
                  <p className="mb-0 text-muted">{data[key] || "N/A"}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ResultCard;
