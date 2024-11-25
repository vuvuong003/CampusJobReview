import React, { useState, useEffect } from "react";
import NavBar from "./Navbar";
import { useNavigate } from "react-router-dom";
import { send_otp_url, unprotected_api_call } from "../api/api";

const ForgotPassword = () => {
    const [otpSent, setOtpSent] = useState(false);
    const [email, setEmail] = useState("");
    const [otp, setOtp] = useState("");
    const [generatedOtp, setGeneratedOtp] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [timeLeft, setTimeLeft] = useState(600); // 10 minutes in seconds

    const navigate = useNavigate();

    const handleClick = async () => {
        if (!otpSent) {
            const newOtp = Math.floor(100000 + Math.random() * 900000).toString();
            setGeneratedOtp(newOtp);
            const requestData = {
                email: email,
                generated_otp: newOtp,
            };

            console.log("Sending OTP...");
            setIsLoading(true);

            let response = await unprotected_api_call(send_otp_url, requestData);

            setIsLoading(false);

            if (response.ok) {
                setOtpSent(true);
                setTimeLeft(600); // Reset timer to 10 minutes
            } else if (response.status === 400) {
                alert("Bad request! The entered email id does not exist.");
            }
        } else {
            console.log("Entered OTP: " + otp);
            if (otp === generatedOtp && timeLeft > 0) {
                navigate("/new-password", { state: { email: email }})
            } else {
                alert("OTP entered is not valid. Try again.");
            }
        }
    };

    // Timer Logic
    useEffect(() => {
        if (otpSent && timeLeft > 0) {
            const timer = setInterval(() => {
                setTimeLeft((prevTime) => prevTime - 1);
            }, 1000);
            return () => clearInterval(timer); // Clear timer on unmount
        } else if (otpSent) {
            alert("OTP expired! Please request a new one");
            setOtpSent(false);
        }
    }, [otpSent, timeLeft]);

    // Format time as MM:SS
    const formatTime = (seconds) => {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
    };

    const myStyle = {
        backgroundImage: `url(${process.env.PUBLIC_URL + "/WolfPlaza.jpg"})`,
        height: "92.5vh",
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        zIndex: -1,
    };

    return (
        <div>
            <NavBar navigation={navigate} />
            <div className="relative h-full w-full">
                <div
                    style={myStyle}
                    className="absolute inset-0 opacity-40 bg-black"
                ></div>
                <div className="fixed inset-0 flex flex-col items-center justify-center mt-20">
                    <h1 className="text-gray-500 text-xl md:text-5xl font-bold mb-8">
                        Forgot Password?
                    </h1>
                    <div className="bg-white w-[40vw] h-[40vh] shadow-lg flex items-center justify-center p-10 overflow-y-auto">
                        <form>
                            <div className="mb-6">
                                <label htmlFor="email" className="block text-gray-700">
                                    Enter email id registered to your account
                                </label>
                                <input
                                    id="email"
                                    type="text"
                                    name="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    aria-label="email"
                                    placeholder="Enter Email"
                                    required
                                />
                            </div>

                            {otpSent && (
                                <div className="mb-6">
                                    <label htmlFor="otp" className="block text-gray-700">
                                        A one-time password has been sent to your email id.
                                    </label>
                                    {/* if the time left is less than a minute, display the timer in red */}
                                    <div className={`text-lg font-bold ${timeLeft <= 60 ? "text-red-500" : "text-black"}`}
                                    >
                                        Time remaining: {formatTime(timeLeft)}
                                    </div>
                                    <input
                                        id="otp"
                                        type="text"
                                        name="otp"
                                        value={otp}
                                        onChange={(e) => setOtp(e.target.value)}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                        aria-label="otp"
                                        placeholder="Enter one-time password"
                                        required
                                    />
                                </div>
                            )}


                            <div className="flex justify-center">
                                {isLoading ? (
                                    <div className="w-6 h-6 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                                ) : (
                                    <button
                                        type="button"
                                        onClick={handleClick}
                                        className="px-6 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600"
                                        aria-label="Submit button"
                                        disabled={otpSent && timeLeft === 0}
                                    >
                                        {otpSent ? "Submit" : "Send OTP"}
                                    </button>
                                )}
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
