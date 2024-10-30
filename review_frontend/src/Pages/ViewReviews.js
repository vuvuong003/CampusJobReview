import * as React from 'react';
import NavBar from './Navbar';
import { useNavigate } from 'react-router-dom';
import { review_url, filter_url, unprotected_api_call } from '../api/api';

class JobRow extends React.Component {
    render() {
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
                    <td><a href="#">{jobTitle}</a></td>
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
                <tr>
                    <td colSpan="10">
                        <hr style={{ borderTop: '1px solid #ccc' }} />
                    </td>
                </tr>
            </>
        );
    }
}

class Reviews extends React.Component {
    state = {
        jobs: [],
        formData: {
            department: '',
            locations: '',
            job_title: '',
            min_rating: '',
            max_rating: '',
        }
    };

    componentDidMount = async () => {
        let response = await unprotected_api_call(filter_url+"/", {}, "GET");
        if (response.status === 200) {
            let data = await response.json();
            this.setState({ jobs: data });
        } else {
            alert("Server Error");
        }
    };

    handleChange = (e) => {
        this.setState({
            formData: {
                ...this.state.formData,
                [e.target.name]: e.target.value,
            },
        });
    };

    handleSubmit = async (e) => {
        e.preventDefault();
        //update the url to have filter parameters
        let fu = filter_url+"/?";
        for (let key in this.state.formData) {
            if (this.state.formData[key] !== "") {
                fu += key + "=" + this.state.formData[key] + "&";
            }

        let response = await unprotected_api_call(fu+"/", {}, "GET");
        if (response.status === 200) {
            let data = await response.json();
            this.setState({ jobs: data });
        } else {
            alert("Server Error");
        }
        
    }
  }

    render() {
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
                    <div style={myStyle} className="absolute inset-0 opacity-40 bg-black"></div>

                    {/* Main content */}
                    <div className="fixed inset-0 flex flex-col items-center justify-center mt-20">
                        <h1 className="text-gray-500 text-xl md:text-5xl font-bold mb-4">
                            Reviews
                        </h1>

                        {/* Filtering Form */}
                        <div className="bg-white w-[70vw] p-4 mb-6 rounded-lg shadow-md justify-">
                            <form onSubmit={this.handleSubmit} className="flex flex-wrap gap-4 items-center">
                                <input
                                    type="text"
                                    name="department"
                                    placeholder="Department"
                                    value={this.state.formData.department}
                                    onChange={this.handleChange}
                                    className="px-4 py-2 border rounded-md w-[18%]"
                                />
                                <input
                                    type="text"
                                    name="locations"
                                    placeholder="Location"
                                    value={this.state.formData.locations}
                                    onChange={this.handleChange}
                                    className="px-4 py-2 border rounded-md w-[18%]"
                                />
                                <input
                                    type="text"
                                    name="job_title"
                                    placeholder="Job Title"
                                    value={this.state.formData.job_title}
                                    onChange={this.handleChange}
                                    className="px-4 py-2 border rounded-md w-[18%]"
                                />
                                <select
                                    name="min_rating"
                                    value={this.state.formData.min_rating}
                                    onChange={this.handleChange}
                                    className="px-4 py-2 border rounded-md w-[18%]"
                                >
                                    <option value="">Min Rating</option>
                                    {[1, 2, 3, 4, 5].map((rating) => (
                                        <option key={rating} value={rating}>{rating}</option>
                                    ))}
                                </select>
                                <select
                                    name="max_rating"
                                    value={this.state.formData.max_rating}
                                    onChange={this.handleChange}
                                    className="px-4 py-2 border rounded-md w-[18%]"
                                >
                                    <option value="">Max Rating</option>
                                    {[1, 2, 3, 4, 5].map((rating) => (
                                        <option key={rating} value={rating}>{rating}</option>
                                    ))}
                                </select>
                                <div className="w-full flex justify-center mt-4">
                                  <button
                                      type="submit"
                                      className="px-4 py-2 bg-blue-500 text-white rounded-md"
                                      onClick={this.handleSubmit}
                                  >
                                      Filter
                                  </button>
                              </div>
                            </form>
                        </div>

                        {/* Review Table */}
                        <div className="bg-white w-[70vw] h-[40vh] shadow-lg flex items-center justify-center p-10 overflow-y-auto">
                            <div className="overflow-x-auto">
                                <table className="min-w-full table-auto border-collapse">
                                    <thead className="bg-gray-200">
                                        <tr>
                                            <th className="px-4 py-2 w-1/5 border">Job Title</th>
                                            <th className="px-4 py-2 w-1/4 border">Job Description</th>
                                            <th className="px-4 py-2 w-1/6 border">Department</th>
                                            <th className="px-4 py-2 w-1/6 border">Location(s)</th>
                                            <th className="px-4 py-2 w-1/12 border">Hourly Pay</th>
                                            <th className="px-4 py-2 w-1/6 border">Employee Benefits</th>
                                            <th className="px-4 py-2 w-1/4 border">Review</th>
                                            <th className="px-4 py-2 w-1/12 border">Rating</th>
                                            <th className="px-4 py-2 w-1/12 border">Recommendation</th>
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

function ReviewsWithNavigate(props) {
    const navigate = useNavigate();
    return <Reviews {...props} navigate={navigate} />;
}

export default ReviewsWithNavigate;
