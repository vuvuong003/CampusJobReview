/**
 * @fileoverview Component for adding job reviews with a form interface
 * Includes fields for job details, ratings, and written review
 */

import * as React from 'react';
import NavBar from './Navbar';
import { useNavigate } from 'react-router-dom';
import { protected_api_call, review_url } from '../api/api';

/**
 * @class AddReview
 * @extends React.Component
 * @description A form component that allows users to submit job reviews
 * including details about position, compensation, and experience
 * 
 * @property {Object} props
 * @property {Function} props.navigate - React Router navigation function
 */
class AddReview extends React.Component {
    /**
     * @state
     * @description Maintains form data for the review submission
     * @property {Object} formData - Contains all form field values
     */
    state = {
        formData: {
            job_title: "",       // Title of the job position
            department: "",      // Department within the organization
            locations: "",       // Location of the job
            job_description: "", // Description of job responsibilities
            hourly_pay: "",      // Hourly compensation
            benefits: "",        // Benefits offered
            rating: "",         // Overall rating (1-5)
            recommendation: "",  // Recommendation score (1-10)
            review: "",         // Detailed written review
        },
    }

    /**
     * Handles changes to form input fields
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
        })
    };

    /**
     * Handles form submission and sends review data to server
     * @method
     * @async
     * @param {Object} e - Form submission event
     * @throws {Error} Displays alert if submission fails
     */
    handleSubmit = async (e) => {
        e.preventDefault();
        let response = await protected_api_call(review_url, this.state.formData);
        if(response.status === 201){
            alert("Review Submitted Successfully");
        }else{
            alert("There was an error submitting your review");
        }
    }
    
    /**
     * Renders the review form component
     * @method
     * @returns {JSX.Element} Rendered component
     */
    render() {
        // Styles for the background image
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
                <NavBar navigation={this.props.navigate}/>
                <div className="relative h-full w-full">
                    {/* Background image with opacity */}
                    <div style={myStyle} className="absolute inset-0 opacity-40 bg-black"></div>

                    {/* Main content */}
                    <div className="fixed inset-0 flex flex-col items-center justify-center mt-20">
                        <h1 className="text-gray-500 text-xl md:text-5xl font-bold mb-8">
                            Add a review
                        </h1>
                        {/* Form container with scroll */}
                        <div className="bg-white w-[40vw] h-[100vh] shadow-lg items-center justify-center p-10 overflow-y-auto">
                            <form onSubmit={this.handleSubmit}>
                                {/* Job Title Input */}
                                <div className="mb-6">
                                    <label htmlFor="job_title" className="block text-gray-700">Job Title</label>
                                    <input
                                        id="job_title"
                                        type="text"
                                        name="job_title"
                                        value={this.state.formData.job_title}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                        aria-required="true"
                                    />
                                </div>

                                {/* Department Input */}
                                <div className="mb-6">
                                    <label htmlFor="department" className="block text-gray-700">Department</label>
                                    <input
                                        id="department"
                                        type="text"
                                        name="department"
                                        value={this.state.formData.department}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                        aria-required="true"
                                    />
                                </div>

                                {/* Location Input */}
                                <div className="mb-6">
                                    <label htmlFor="locations" className="block text-gray-700">Location</label>
                                    <input
                                        id="locations"
                                        type="text"
                                        name="locations"
                                        value={this.state.formData.locations}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                        aria-required="true"
                                    />
                                </div>

                                {/* Job Description Input */}
                                <div className="mb-6">
                                    <label htmlFor="job_description" className="block text-gray-700">Job Description</label>
                                    <input
                                        id="job_description"
                                        type="text"
                                        name="job_description"
                                        value={this.state.formData.job_description}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                        aria-required="true"
                                    />
                                </div>

                                {/* Hourly Pay Input */}
                                <div className="mb-6">
                                    <label htmlFor="hourly_pay" className="block text-gray-700">Hourly Pay</label>
                                    <input
                                        id="hourly_pay"
                                        type="text"
                                        name="hourly_pay"
                                        value={this.state.formData.hourly_pay}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                        aria-required="true"
                                    />
                                </div>

                                {/* Benefits Input */}
                                <div className="mb-6">
                                    <label htmlFor="benefits" className="block text-gray-700">Benefits</label>
                                    <input
                                        id="benefits"
                                        type="text"
                                        name="benefits"
                                        value={this.state.formData.benefits}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                        aria-required="true"
                                    />
                                </div>

                                {/* Rating Radio Buttons */}
                                <div className="mb-6">
                                    <fieldset>
                                        <legend className="block text-gray-700 mb-2">Rating</legend>
                                        <div className="flex space-x-4 mt-2">
                                            {[1, 2, 3, 4, 5].map((rating) => (
                                                <label key={rating} className="inline-flex items-center" htmlFor={`rating-${rating}`}>
                                                    <input
                                                        id={`rating-${rating}`}
                                                        type="radio"
                                                        name="rating"
                                                        value={rating}
                                                        onChange={this.handleChange}
                                                        className="form-radio"
                                                        aria-label={`Rating ${rating}`}
                                                    />
                                                    <span className="ml-2">{rating}</span>
                                                </label>
                                            ))}
                                        </div>
                                    </fieldset>
                                </div>

                                {/* Recommendation Radio Buttons */}
                                <div className="mb-6">
                                    <fieldset>
                                        <legend className="block text-gray-700 mb-2">Recommendation</legend>
                                        <div className="flex space-x-4 mt-2">
                                            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((recommendation) => (
                                                <label key={recommendation} className="inline-flex items-center" htmlFor={`recommendation-${recommendation}`}>
                                                    <input
                                                        id={`recommendation-${recommendation}`}
                                                        type="radio"
                                                        name="recommendation"
                                                        value={recommendation}
                                                        onChange={this.handleChange}
                                                        className="form-radio"
                                                        aria-label={`Recommendation ${recommendation}`}
                                                    />
                                                    <span className="ml-2">{recommendation}</span>
                                                </label>
                                            ))}
                                        </div>
                                    </fieldset>
                                </div>

                                {/* Review Text Area */}
                                <div className="mb-6">
                                    <label htmlFor="review" className="block text-gray-700">Review</label>
                                    <textarea
                                        id="review"
                                        name="review"
                                        value={this.state.formData.review}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                        aria-required="true"
                                    />
                                </div>

                                {/* Submit Button */}
                                <div className="flex justify-center">
                                    <button
                                        type="submit"
                                        className="px-6 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600"
                                        aria-label="Submit your review"
                                    >
                                        Submit your review
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
 * Higher-order component that wraps AddReview with navigation capabilities
 * @function
 * @param {Object} props - Component props
 * @returns {JSX.Element} AddReview component with navigation prop
 */
function AddReviewWithNavigate(props) {
    const navigate = useNavigate();
    return <AddReview {...props} navigate={navigate} />;
}

export default AddReviewWithNavigate;
export { AddReview };