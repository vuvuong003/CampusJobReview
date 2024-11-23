/**
 * @fileoverview Signup component for user registration
 * Handles new user account creation and form validation
 */

import * as React from "react";
import NavBar from "./Navbar";
import { useNavigate } from "react-router-dom";
import { register_url, unprotected_api_call } from "../api/api";

/**
 * @class Signup
 * @extends React.Component
 * @description Component for handling new user registration
 *
 * @property {Object} props
 * @property {Function} props.navigate - React Router navigation function
 */
class Signup extends React.Component {
  /**
   * @state
   * @description Maintains form data for user registration
   * @property {Object} formData - Contains username and password fields
   */
  state = {
    formData: {
      password: "", // User's password
      email: "", // User's email
      username: "", // User's username
    },
  };

  /**
   * Handles changes to signup form input fields
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
   * Handles form submission for user registration
   * @method
   * @async
   * @param {Object} e - Form submission event
   * @description Attempts to register new user with provided credentials
   *              On success: Redirects to login page
   *              On failure: Shows error message if user already exists
   */
  handleSubmit = async (e) => {
    e.preventDefault();
    console.log(this.state.formData);
    let response = await unprotected_api_call(
      register_url,
      this.state.formData,
    );
    if (response.status === 200) {
      alert("Registration successful");
      this.props.navigate("/login");
    } else {
      alert("User Exists");
    }
  };

  /**
   * Renders the signup form component
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
              Sign Up
            </h1>
            {/* Signup form container */}
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

                <div className="mb-6">
                  <label htmlFor="username" className="block text-gray-700">
                    Email
                  </label>
                  <input
                    id="email"
                    type="text"
                    name="email"
                    value={this.state.formData.email}
                    onChange={this.handleChange}
                    className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                    aria-label="Email"
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
                    password={true}
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
                    aria-label="Sign up button"
                  >
                    Sign Up
                  </button>
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
 * Higher-order component that wraps Signup with navigation capabilities
 * @function SignupWithNavigate
 * @param {Object} props - Component props
 * @returns {JSX.Element} Signup component with navigation prop
 */
function SignupWithNavigate(props) {
  const navigate = useNavigate();
  return <Signup {...props} navigate={navigate} />;
}

export default SignupWithNavigate;
// export default AddReview;
