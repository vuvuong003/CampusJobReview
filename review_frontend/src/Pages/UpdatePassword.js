import { useState } from "react";
import NavBar from "./Navbar";
import { useLocation, useNavigate } from "react-router-dom";
import { update_password_url, unprotected_api_call } from "../api/api";

const UpdatePassword = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false); // State for toggling password visibility

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    const handleSubmit = async (e) => {
        console.log("submitted");
        const { email } = location.state || {};

        console.log("email : " + email);

        if (newPassword === confirmPassword) {
            console.log("passwords match");
            const requestData = {
                "email": email,
                "password": newPassword
            };
    
            const response = await unprotected_api_call(update_password_url, requestData);
    
            if (response.ok) {
                alert("Password successfully changed!");
                navigate("/login");
            } else {
                alert(`${response.json()["message"]}`)
            }
        } else {
            alert("Password does not match! Make sure you enter the same password");
        }
    }

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
                        Enter new password
                    </h1>
                    <div className="bg-white w-[40vw] h-[40vh] shadow-lg flex items-center justify-center p-10 overflow-y-auto">
                        <form>
                            {/* New Password Field */}
                            <div className="mb-6">
                                <label htmlFor="new_password" className="block text-gray-700">
                                    Please enter new password for your account.
                                </label>
                                <input
                                    id="new_password"
                                    type="password"
                                    name="new_password"
                                    value={newPassword}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                    className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    aria-label="new_password"
                                    placeholder="Enter password"
                                    required
                                />
                            </div>

                            {/* Confirm Password Field */}
                            <div className="mb-6 relative">
                                <input
                                    id="confirm_password"
                                    type={showPassword ? "text" : "password"} // Toggles input type
                                    name="confirm_password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    aria-label="confirm_password"
                                    placeholder="Confirm password"
                                    required
                                />
                                {/* Eye Icon/Button for Toggling */}
                                <button
                                    type="button"
                                    onClick={togglePasswordVisibility}
                                    className="absolute right-3 top-3 text-gray-500 hover:text-gray-700 focus:outline-none"
                                    aria-label="Toggle password visibility"
                                >
                                    {showPassword ? "🙈" : "👁️"}
                                </button>
                            </div>

                            {/* Submit Button */}
                            <div className="flex justify-center">
                                <button
                                    type="button"
                                    onClick={handleSubmit}
                                    className="px-6 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600"
                                    aria-label="Submit button"
                                >
                                    Submit
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UpdatePassword;
