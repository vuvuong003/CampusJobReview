/**
 * @fileoverview Home page component for NC State Campus Jobs
 * Provides navigation to review management features with authentication checks
 */

import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import NavBar from './Navbar';

/**
 * @class Home
 * @extends React.Component
 * @description Main landing page component with navigation to add and view reviews
 * 
 * @property {Object} props
 * @property {Function} props.navigate - React Router navigation function
 */
class Home extends React.Component {
    /**
     * Handles navigation to add review page with authentication check
     * @method
     * @description Verifies user is logged in before allowing access to add review page
     * @returns {void}
     */
    add_review = () => {
        // check if login is true in local storage
        let login = localStorage.getItem("login")
        if (login === "true") {
            this.props.navigate('/add-review')
        } else {
            alert("Please login to add reviews")
            // this.props.navigate('/login')
        }
    }

    /**
     * Handles navigation to view reviews page with authentication check
     * @method
     * @description Verifies user is logged in before allowing access to view reviews page
     * @returns {void}
     */
    view_reviews = () => {
        // check if login is true in local storage
        let login = localStorage.getItem("login")
        if (login !== "true") {
            alert("Please login to view reviews")
            // this.props.navigate('/login')
        }else{
            this.props.navigate('/view-reviews')
        }
    }
    
    /**
     * Renders the home page component
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
            backgroundImage: `url(${
                process.env.PUBLIC_URL + "/WolfPlaza.jpg"
            })`,
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
                <NavBar navigation={this.props.navigate}/>
                <div className="relative h-full w-full">
                    {/* Background image with opacity */}
                    <div style={myStyle} className="opacity-40 bg-black"></div>

                    {/* Main content container */}
                    <div className="relative z-10 flex flex-col items-center justify-center h-full text-center">
                        {/* Page Title */}
                        <h1 className="text-gray-900 text-2xl md:text-5xl font-bold mb-8 mt-20">
                            NC State Campus Jobs
                        </h1>
                        {/* Navigation Buttons */}
                        <div className="flex space-x-8 mt-20">
                            <button 
                                className="bg-red-500 hover:bg-red-200 text-white font-bold py-2 px-4 rounded-lg" 
                                onClick={() => this.add_review()}
                                aria-label="Add Reviews - Login required"
                            >
                                Add Reviews
                            </button>
                            <button 
                                className="bg-red-500 hover:bg-red-200 text-white font-bold py-2 px-4 rounded-lg" 
                                onClick={() => this.view_reviews()}
                                aria-label="View Reviews - Login required"
                            >
                                View Reviews
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

/**
 * Higher-order component that wraps Home with navigation capabilities
 * @function HomeWithNavigate
 * @param {Object} props - Component props
 * @returns {JSX.Element} Home component with navigation prop
 */
function HomeWithNavigate(props) {
    const navigate = useNavigate();
    return <Home {...props} navigate={navigate} />;
}

export default HomeWithNavigate;