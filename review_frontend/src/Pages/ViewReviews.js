/**
 * @fileoverview Reviews display and filtering components
 * Contains components for displaying job reviews in a collapsible table format with filtering capabilities
 */

import * as React from "react";
import NavBar from "./Navbar";
import { useNavigate } from "react-router-dom";
import { review_url, all_reviews_url, unprotected_api_call } from "../api/api";
import Comments from "./Comments";

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

  /**
   * Toggles the expanded state of the job review row
   * @method
   */
  toggleExpand = () => {
    this.setState((prevState) => ({ isExpanded: !prevState.isExpanded }));
  };

  render() {
    // Destructure props for cleaner access
    const {
      reviewId,
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
      currentUser
    } = this.props;
    const { isExpanded } = this.state;

    return (
      <div className="job-row bg-white shadow-lg rounded-lg p-6 mb-6 transition-all duration-300 ease-in-out hover:shadow-xl">
        <div className="job-summary flex justify-between items-center">
          <h3 className="job-title text-2xl font-semibold text-gray-800">
            <a
              onClick={this.toggleExpand}
              className="hover:text-blue-500 focus:outline-none"
              style={{ cursor: "pointer" }}
            >
              {jobTitle} (${hourlyPay}/hr)
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
            <div className="job-details p-4 border border-gray-300 rounded-lg">
                  {/* Job Review Section */}
                  <div className="job-review mb-4">
                    <p className="text-lg text-left font-semibold text-gray-800">
                      <strong>Reviewed By:</strong> {reviewedBy}
                    </p>
                    <p className="text-lg text-left text-gray-600">{review}</p>
                  </div>

                  {/* Job Description */}
                  <div className="job-description mb-4">
                    <p className="text-lg text-left font-semibold text-gray-800">
                      <strong>Job Description:</strong> {jobDescription}
                    </p>
                  </div>

                  {/* Category Row with Circular Boxes */}
                  <div className="categories flex flex-wrap gap-4">
                    <div
                      className="category bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium"
                      style={{ display: 'inline-block' }}
                    >
                      Department: {department}
                    </div>
                    <div
                      className="category bg-green-100 text-green-700 px-4 py-2 rounded-full text-sm font-medium"
                      style={{ display: 'inline-block' }}
                    >
                      Location: {location}
                    </div>
                    <div
                      className="category bg-yellow-100 text-yellow-700 px-4 py-2 rounded-full text-sm font-medium"
                      style={{ display: 'inline-block' }}
                    >
                      Benefits: {benefits}
                    </div>
                    <div
                      className="category bg-purple-100 text-purple-700 px-4 py-2 rounded-full text-sm font-medium"
                      style={{ display: 'inline-block' }}
                    >
                      Recommendation: {recommendation}
                    </div>
                  </div>
                </div>
            <Comments reviewId={reviewId} currentUser={currentUser}/>
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
    allJobs: [],
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
    let response = await unprotected_api_call(all_reviews_url, {}, "GET");
    if (response.status === 200) {
      let data = await response.json();
      this.setState({ allJobs: data, jobs: data });
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
   * Handles filter form submsision and updates job listings
   * @method
   * @param {Object} e - Form submission event
   * @description Creates a new job list initiated to the origina list and filters out the unrequired jobs
   */
  handleSubmit = async (e) => {
    e.preventDefault();

    // get the original list of all job reviews
    const jobs = this.state.allJobs;

    // a copy of the original list which will contain the filtered job reviews
    let updatedList = jobs;

    for (let key in this.state.formData) {
      if (this.state.formData[key] !== "") {
        if (key == "department" || key == "locations" || key == "job_title"){
          updatedList = [...updatedList].filter((job) => String(job[key]).toLowerCase().includes(this.state.formData[key].toLowerCase()));
        } else if (key == "min_rating") {
          updatedList = [...updatedList].filter((job) => job.rating >= Number(this.state.formData[key]));
        } else {
          updatedList = [...updatedList].filter((job) => job.rating <= Number(this.state.formData[key]));
        }
      }
    }

    this.setState({ jobs: updatedList })
  }

  /**
   * Handles resetting the filters
   * @method
   */
  handleReset = () => {
    const allJobs = this.state.allJobs;
    // Reset the form fields
    this.setState(
      {
        formData: {
          department: "",
          locations: "",
          job_title: "",
          min_rating: "",
          max_rating: "",
        },

        jobs:allJobs,
      },
    );
  };

  render() {
    const currentUser = localStorage.getItem("current_user");

    return (
      <div>
        <NavBar navigation={this.props.navigate} />
        <div className="relative h-full w-full" style={{ backgroundColor: "#ffe5e5"}}>
          {/* <div style={myStyle} className="absolute inset-0 opacity-40 bg-black"></div> */}

          {/* Main content container */}
          <div className="flex w-full h-full">
            {/* Left side: Filters */}
            <div className="w-1/4 p-6">
              <div className="bg-white shadow-lg p-6 rounded-xl mb-6">
                <form
                  onSubmit={this.handleSubmit}
                  className="flex flex-col gap-4"
                >
                  {/* Department filter */}
                  <input
                    type="text"
                    name="department"
                    placeholder="Department"
                    value={this.state.formData.department}
                    onChange={this.handleChange}
                    className="px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {/* Location filter */}
                  <input
                    type="text"
                    name="locations"
                    placeholder="Location"
                    value={this.state.formData.locations}
                    onChange={this.handleChange}
                    className="px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                   {/* Job title filter */}
                  <input
                    type="text"
                    name="job_title"
                    placeholder="Job Title"
                    value={this.state.formData.job_title}
                    onChange={this.handleChange}
                    className="px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {/* Minimum rating filter */}
                  <select
                    name="min_rating"
                    aria-label="Min Rating"
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
                  {/* Maximum rating filter */}
                  <select
                    name="max_rating"
                    aria-label="Max Rating"
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
                  {/* Filter button */}
                  <button
                    type="submit"
                    className="bg-blue-500 text-white py-3 rounded-lg"
                  >
                    Filter
                  </button>
                   {/* Reset Button */}
                  <button
                    type="button"
                    onClick={this.handleReset}
                    className="bg-red-500 text-white py-3 rounded-lg"
                  >
                    Reset
                  </button>
                </form>
              </div>
            </div>

            {/* Right side: Job Listings */}
            <div className="w-3/4 p-6 overflow-y-auto flex-1">
              {this.state.jobs.map((job, index) => (
                <JobRow
                  key={index}
                  reviewId = {job.id}
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
                  currentUser={currentUser}
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
