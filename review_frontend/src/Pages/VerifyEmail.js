import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { unprotected_api_call, base_url } from "../api/api";

const VerifyEmail = () => {
  const [status, setStatus] = useState("Verifying...");
  const { uid, token } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const verificationUrl = `${base_url}auth/verify-email/${uid}/${token}/`;
        console.log("Verification Link:", verificationUrl);
        const response = await unprotected_api_call(verificationUrl, {}, "GET");

        if (response.ok) {
          const data = await response.json();
          setStatus("Email verified successfully! You can now login.");
          setTimeout(() => navigate("/login"), 3000);
        } else {
          const errorData = await response.json();
          setStatus(
            "Verification failed. Please try again or contact support."
          );
        }
      } catch (error) {
        console.error("Verification error:", error);
        setStatus("An error occurred during verification.");
      }
    };

    verifyEmail();
  }, [uid, token, navigate]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="bg-white p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Email Verification</h2>
        <p className="text-gray-600">{status}</p>
      </div>
    </div>
  );
};

export default VerifyEmail;
