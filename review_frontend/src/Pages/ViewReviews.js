/**
 * @fileoverview Reviews display and filtering components
 * Contains components for displaying job reviews in a table format with filtering capabilities
 */

import * as React from "react";
import NavBar from "./Navbar";
import { useNavigate } from "react-router-dom";
import { unprotected_api_call, filter_url } from "../api/api";

/**
 * @class JobRow
 * @extends React.Component
 * @description Renders a single job review entry in the reviews table
 *
 * @property {Object} props
 * @property {string} props.jobTitle - Title of the job position
 * @property {string} props.jobDescription - Description of the job responsibilities
 * @property {string} props.department - Department where job is located
 * @property {string} props.location - Physical location of the job
 * @property {string} props.hourlyPay - Hourly compensation
 * @property {string} props.benefits - Employee benefits package
 * @property {string} props.review - Written review content
 * @property {number} props.rating - Numerical rating (1-5)
 * @property {number} props.recommendation - Recommendation score
 * @property {string} props.reviewedBy - Username of reviewer
 */
class JobRow extends React.Component {
  state = {
    isExpanded: false, // To track the expanded state of the row
  };

  toggleExpand = () => {
    this.setState((prevState) => ({ isExpanded: !prevState.isExpanded }));
  };

  render() {
    // Destructure props for cleaner access
    const {
      jobTitle,
      jobDescription,
      department,
      location,
      hourlyPay,
      benefits,
      review,
      rating,
      recommendation,
      reviewedBy,
    } = this.props;
    const { isExpanded } = this.state;

    return (
      <div className="job-row bg-white shadow-lg rounded-lg p-6 mb-6 transition-all duration-300 ease-in-out hover:shadow-xl">
        <div className="job-summary flex justify-between items-center">
          <h3 className="job-title text-2xl font-semibold text-gray-800">
            <a
              href="#"
              onClick={this.toggleExpand}
              className="hover:text-blue-500 focus:outline-none"
            >
              {jobTitle}
            </a>
          </h3>
          <div className="flex items-center space-x-2">
            <span className="text-yellow-400 text-2xl">
              {'★'.repeat(rating)}
              <span className="text-gray-400">
                {'★'.repeat(5 - rating)}
              </span>
            </span>
            <span className="ml-2 text-gray-500 cursor-pointer" onClick={this.toggleExpand}>
              {isExpanded ? "▲" : "▼"}
            </span>
          </div>
        </div>
        {isExpanded && (
          <div className="job-details mt-4 text-gray-600">
            <p><strong>Job Description:</strong> {jobDescription}</p>
            <p><strong>Department:</strong> {department}</p>
            <p><strong>Location:</strong> {location}</p>
            <p><strong>Hourly Pay:</strong> ${hourlyPay}</p>
            <p><strong>Benefits:</strong> {benefits}</p>
            <p><strong>Review:</strong> {review}</p>
            <p><strong>Rating:</strong> {rating}</p>
            <p><strong>Recommendation:</strong> {recommendation}</p>
            <p><strong>Reviewed By:</strong> {reviewedBy}</p>
          </div>
        )}
      </div>
    );    
  }
}

/**
 * @class Reviews
 * @extends React.Component
 * @description Main component for displaying and filtering job reviews
 */
class Reviews extends React.Component {
   /**
   * @state
   * @property {Array<Object>} jobs - Array of job review objects
   * @property {Object} formData - Filter criteria for reviews
   * @property {string} formData.department - Filter by department name
   * @property {string} formData.locations - Filter by job location
   * @property {string} formData.job_title - Filter by job title
   * @property {string} formData.min_rating - Minimum rating filter
   * @property {string} formData.max_rating - Maximum rating filter
   */
  state = {
    jobs: [],
    formData: {
      department: "",
      locations: "",
      job_title: "",
      min_rating: "",
      max_rating: "",
    },
  };

  /**
   * Fetches initial job reviews data when component mounts
   * @method
   * @async
   */
  componentDidMount = async () => {
    let response = await unprotected_api_call(filter_url + "/", {}, "GET");
    if (response.status === 200) {
      let data = await response.json();
      this.setState({ jobs: data });
      console.log("Data: ", data);
    } else {
      alert("Server Error");
    }
  };

  /**
   * Handles changes to filter form inputs
   * @method
   * @param {Object} e - Input change event
   * @param {string} e.target.name - Name of the changed input field
   * @param {string} e.target.value - New value of the input field
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
   * Handles filter form submission and updates job listings
   * @method
   * @async
   * @param {Object} e - Form submission event
   * @description Constructs URL with filter parameters and fetches filtered results
   */
  handleSubmit = async (e) => {
    e.preventDefault();
    //update the url to have filter parameters
    let fu = filter_url + "/?";
    // Add non-empty filter parameters to URL
    for (let key in this.state.formData) {
      if (this.state.formData[key] !== "") {
        fu += key + "=" + this.state.formData[key] + "&";
      }
    }

    let response = await unprotected_api_call(fu + "/", {}, "GET");
    if (response.status === 200) {
      let data = await response.json();
      this.setState({ jobs: data });
    } else {
      alert("Server Error");
    }
  };

  render() {
    // Background image styles
    const myStyle = {
      backgroundImage: `url(${process.env.PUBLIC_URL + "/WolfPlaza.jpg"})`,
      height: "100vh",
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
        <NavBar navigation={this.props.navigate} />
        <div className="relative h-full w-full">
          <div style={myStyle} className="absolute inset-0 opacity-40 bg-black"></div>

          {/* Main content container */}
          <div className="flex w-full h-full">
            {/* Left side: Filters */}
            <div className="w-1/4 p-6">
              <div className="bg-white shadow-lg p-6 rounded-xl mb-6">
                <form
                  onSubmit={this.handleSubmit}
                  className="flex flex-col gap-4"
                >
                  <input
                    type="text"
                    name="department"
                    placeholder="Department"
                    value={this.state.formData.department}
                    onChange={this.handleChange}
                    className="px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <input
                    type="text"
                    name="locations"
                    placeholder="Location"
                    value={this.state.formData.locations}
                    onChange={this.handleChange}
                    className="px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <input
                    type="text"
                    name="job_title"
                    placeholder="Job Title"
                    value={this.state.formData.job_title}
                    onChange={this.handleChange}
                    className="px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <select
                    name="min_rating"
                    value={this.state.formData.min_rating}
                    onChange={this.handleChange}
                    className="px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Min Rating</option>
                    {[1, 2, 3, 4, 5].map((rating) => (
                      <option key={rating} value={rating}>
                        {rating}
                      </option>
                    ))}
                  </select>
                  <select
                    name="max_rating"
                    value={this.state.formData.max_rating}
                    onChange={this.handleChange}
                    className="px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Max Rating</option>
                    {[1, 2, 3, 4, 5].map((rating) => (
                      <option key={rating} value={rating}>
                        {rating}
                      </option>
                    ))}
                  </select>
                  <button
                    type="submit"
                    className="bg-blue-500 text-white py-3 rounded-lg"
                  >
                    Filter
                  </button>
                </form>
              </div>
            </div>

            {/* Right side: Job Listings */}
            <div className="w-3/4 p-6 overflow-y-auto flex-1">
              {this.state.jobs.map((job, index) => (
                <JobRow
                  key={index}
                  jobTitle={job.job_title}
                  jobDescription={job.job_description}
                  department={job.department}
                  location={job.locations}
                  hourlyPay={job.hourly_pay}
                  benefits={job.benefits}
                  review={job.review}
                  rating={job.rating}
                  recommendation={job.recommendation}
                  reviewedBy={job.reviewed_by}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

/**
 * Higher-order component that wraps Reviews with navigation capabilities
 * @function ReviewsWithNavigate
 * @param {Object} props - Component props
 * @returns {JSX.Element} Reviews component with navigation prop
 */
function ReviewsWithNavigate(props) {
  const navigate = useNavigate();
  return <Reviews {...props} navigate={navigate} />;
}

export default ReviewsWithNavigate;
