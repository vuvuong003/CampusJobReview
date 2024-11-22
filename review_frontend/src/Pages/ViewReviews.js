/**
 * @fileoverview Reviews display and filtering components
 * Contains components for displaying job reviews in a table format with filtering capabilities
 */

import * as React from "react";
import NavBar from "./Navbar";
import { useNavigate } from "react-router-dom";
import { review_url, all_reviews_url, unprotected_api_call } from "../api/api";

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

    return (
      <>
        <tr>
          <td>
            <a href="#">{jobTitle}</a>
          </td>
          <td>{jobDescription}</td>
          <td>{department}</td>
          <td>{location}</td>
          <td>{hourlyPay}</td>
          <td>{benefits}</td>
          <td>{review}</td>
          <td>{rating}</td>
          <td>{recommendation}</td>
          <td>{reviewedBy}</td>
        </tr>
        {/* Separator line between rows */}
        <tr>
          <td colSpan="10">
            <hr style={{ borderTop: "1px solid #ccc" }} />
          </td>
        </tr>
      </>
    );
  }
}

/**
 * @class Reviews
 * @extends React.Component
 * @description Main component for displaying and filtering job reviews
 *
 * @property {Object} props
 * @property {Function} props.navigate - React Router navigation function
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
          updatedList = [...updatedList].filter((job) => String(job[key]).includes(this.state.formData[key]));
        } else if (key == "min_rating") {
          updatedList = [...updatedList].filter((job) => job.rating >= Number(this.state.formData[key]));
        } else {
          updatedList = [...updatedList].filter((job) => job.rating <= Number(this.state.formData[key]));
        }
      }
    }

    this.setState({ jobs: updatedList })
  }

  render() {
    // Background image styles
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
        <NavBar navigation={this.props.navigate} />
        <div className="relative h-full w-full">
          {/* Background image with opacity */}
          <div
            style={myStyle}
            className="absolute inset-0 opacity-40 bg-black"
          ></div>

          {/* Main content container */}
          <div className="fixed inset-0 flex flex-col items-center justify-center mt-20">
            <h1 className="text-gray-500 text-xl md:text-5xl font-bold mb-4">
              Reviews
            </h1>

            {/* Filter form section */}
            <div className="bg-white w-[70vw] p-4 mb-6 rounded-lg shadow-md justify-">
              <form
                onSubmit={this.handleSubmit}
                className="flex flex-wrap gap-4 items-center"
              >
                {/* Department filter */}
                <input
                  type="text"
                  name="department"
                  placeholder="Department"
                  value={this.state.formData.department}
                  onChange={this.handleChange}
                  className="px-4 py-2 border rounded-md w-[18%]"
                  aria-label="Filter by department"
                />
                {/* Location filter */}
                <input
                  type="text"
                  name="locations"
                  placeholder="Location"
                  value={this.state.formData.locations}
                  onChange={this.handleChange}
                  className="px-4 py-2 border rounded-md w-[18%]"
                  aria-label="Filter by location"
                />
                {/* Job title filter */}
                <input
                  type="text"
                  name="job_title"
                  placeholder="Job Title"
                  value={this.state.formData.job_title}
                  onChange={this.handleChange}
                  className="px-4 py-2 border rounded-md w-[18%]"
                  aria-label="Filter by job title"
                />
                {/* Minimum rating filter */}
                <select
                  name="min_rating"
                  value={this.state.formData.min_rating}
                  onChange={this.handleChange}
                  className="px-4 py-2 border rounded-md w-[18%]"
                  aria-label="Filter by minimum rating"
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
                  value={this.state.formData.max_rating}
                  onChange={this.handleChange}
                  className="px-4 py-2 border rounded-md w-[18%]"
                  aria-label="Filter by maximum rating"
                >
                  <option value="">Max Rating</option>
                  {[1, 2, 3, 4, 5].map((rating) => (
                    <option key={rating} value={rating}>
                      {rating}
                    </option>
                  ))}
                </select>
                {/* Filter button */}
                <div className="w-full flex justify-center mt-4">
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-500 text-white rounded-md"
                    onClick={this.handleSubmit}
                    aria-label="Apply filters"
                  >
                    Filter
                  </button>
                </div>
              </form>
            </div>

            {/* Reviews table section */}
            <div className="bg-white w-[70vw] h-[40vh] shadow-lg items-center justify-center p-10 overflow-y-auto">
              <div className="overflow-x-auto">
                <table
                  className="min-w-full table-auto border-collapse"
                  role="table"
                  aria-label="Job Reviews"
                >
                  <thead className="bg-gray-200">
                    <tr>
                      <th className="px-4 py-2 w-1/5 border">Job Title</th>
                      <th className="px-4 py-2 w-1/4 border">
                        Job Description
                      </th>
                      <th className="px-4 py-2 w-1/6 border">Department</th>
                      <th className="px-4 py-2 w-1/6 border">Location(s)</th>
                      <th className="px-4 py-2 w-1/12 border">Hourly Pay</th>
                      <th className="px-4 py-2 w-1/6 border">
                        Employee Benefits
                      </th>
                      <th className="px-4 py-2 w-1/4 border">Review</th>
                      <th className="px-4 py-2 w-1/12 border">Rating</th>
                      <th className="px-4 py-2 w-1/12 border">
                        Recommendation
                      </th>
                      <th className="px-4 py-2 w-1/6 border">Reviewed By</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-300">
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
                  </tbody>
                </table>
              </div>
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
