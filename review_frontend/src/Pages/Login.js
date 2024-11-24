/**
 * @fileoverview Login component for user authentication
 * Handles user credentials and authentication state management
 */

import * as React from "react";
import NavBar from "./Navbar";
import { useNavigate, Link } from "react-router-dom";
import { login_url, unprotected_api_call } from "../api/api";

/**
 * @class Login
 * @extends React.Component
 * @description Component for handling user authentication
 *
 * @property {Object} props
 * @property {Function} props.navigate - React Router navigation function
 */
class Login extends React.Component {
  /**
   * @state
   * @description Maintains form data for login credentials
   * @property {Object} formData - Contains username and password
   */
  state = {
    formData: {
      username: "", // User's username
      password: "", // User's password
    },
  };

  /**
   * Handles changes to login form input fields
   * @method
   * @param {Object} e - Event object from form input change
   * @param {string} e.target.name - Name of the form field
   * @param {string} e.target.value - New value of the form field
   */
  handleChange = (e) => {
    this.setState({
      formData: {
        ...this.state.formData,
        [e.target.name]: e.target.value,
      },
    });
  };

  /**
   * Handles form submission and authentication
   * @method
   * @async
   * @param {Object} e - Form submission event
   * @description Attempts to authenticate user with provided credentials
   *              On success: Stores user data and auth token in localStorage
   *              On failure: Shows error message
   */
  handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let response = await unprotected_api_call(login_url, this.state.formData);

      if (response.ok) {
        let data = await response.json();
        if (data.data && data.data.val) {
          localStorage.setItem("user_data", JSON.stringify(data));
          localStorage.setItem("login", "true");
          this.props.navigate("/");
        } else {
          alert("Login failed. Please verify your email first.");
        }
      } else {
        const errorData = await response.json();
        alert(errorData.detail || "Invalid Credentials");
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("Server Error. Please try again later.");
    }
  };

  /**
   * Renders the login form component
   * @method
   * @returns {JSX.Element} Rendered component
   */
  render() {
    /**
     * Styles for the background image
     * @constant
     * @type {Object}
     */
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
        {/* Navigation Bar */}
        <NavBar navigation={this.props.navigate} />
        <div className="relative h-full w-full">
          {/* Background image with opacity */}
          <div
            style={myStyle}
            className="absolute inset-0 opacity-40 bg-black"
          ></div>

          {/* Main content container */}
          <div className="fixed inset-0 flex flex-col items-center justify-center mt-20">
            <h1 className="text-gray-500 text-xl md:text-5xl font-bold mb-8">
              Login
            </h1>
            {/* Login form container */}
            <div className="bg-white w-[40vw] h-[40vh] shadow-lg flex items-center justify-center p-10 overflow-y-auto">
              <form onSubmit={this.handleSubmit}>
                {/* Username input field */}
                <div className="mb-6">
                  <label htmlFor="username" className="block text-gray-700">
                    Username
                  </label>
                  <input
                    id="username"
                    type="text"
                    name="username"
                    value={this.state.formData.username}
                    onChange={this.handleChange}
                    className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                    aria-label="Username"
                    required
                  />
                </div>

                {/* Password input field */}
                <div className="mb-6">
                  <label htmlFor="password" className="block text-gray-700">
                    Password
                  </label>
                  <input
                    id="password"
                    type="password"
                    name="password"
                    value={this.state.formData.password}
                    onChange={this.handleChange}
                    className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                    aria-label="Password"
                    required
                  />
                </div>

                {/* Submit button */}
                <div className="flex justify-center">
                  <button
                    type="submit"
                    className="px-6 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600"
                    aria-label="Login button"
                  >
                    Login
                  </button>
                </div>
                <div className="flex justify-center">
                  <Link to="/forgot-password" className="w-full px-4 py-2 mt-2">
                    Forgot Password?
                  </Link>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

/**
 * Higher-order component that wraps Login with navigation capabilities
 * @function LoginWithNavigate
 * @param {Object} props - Component props
 * @returns {JSX.Element} Login component with navigation prop
 */
function LoginWithNavigate(props) {
  const navigate = useNavigate();
  return <Login {...props} navigate={navigate} />;
}

export default LoginWithNavigate;
