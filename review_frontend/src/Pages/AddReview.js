import * as React from 'react';
import NavBar from './Navbar';
import { useNavigate } from 'react-router-dom';
import { protected_api_call, review_url } from '../api/api';

class AddReview extends React.Component {

    state = {
        formData: {
            job_title: "",
            department: "",
            locations: "",
            job_description: "",
            hourly_pay: "",
            benefits: "",
            rating: "",
            recommendation: "",
            review: "",
        },
    }

    handleChange = (e) => {
        this.setState({
            formData: {
                ...this.state.formData,
                [e.target.name]: e.target.value,
            },
        })
    };

    handleSubmit = async (e) => {
        e.preventDefault();
        let response = await protected_api_call(review_url, this.state.formData);
        if(response.status === 201){
            alert("Review Submitted Successfully");
        }else{
            alert("There was an error submitting your review");
        }
    }
    
    render() {
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
                        <div className="bg-white w-[40vw] h-[100vh] shadow-lg items-center justify-center p-10 overflow-y-auto">
                            <form onSubmit={this.handleSubmit}>
                                <div className="mb-6">
                                    <label className="block text-gray-700">Job Title</label>
                                    <input
                                        type="text"
                                        name="job_title"
                                        value={this.state.formData.job_title}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    />
                                </div>

                                <div className="mb-6">
                                    <label className="block text-gray-700">Department</label>
                                    <input
                                        type="text"
                                        name="department"
                                        value={this.state.formData.department}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    />
                                </div>

                                <div className="mb-6">
                                    <label className="block text-gray-700">Location</label>
                                    <input
                                        type="text"
                                        name="locations"
                                        value={this.state.formData.locations}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    />
                                </div>

                                <div className="mb-6">
                                    <label className="block text-gray-700">Job Description</label>
                                    <input
                                        type="text"
                                        name="job_description"
                                        value={this.state.formData.job_description}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    />
                                </div>

                                <div className="mb-6">
                                    <label className="block text-gray-700">Hourly Pay</label>
                                    <input
                                        type="text"
                                        name="hourly_pay"
                                        value={this.state.formData.hourly_pay}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    />
                                </div>

                                <div className="mb-6">
                                    <label className="block text-gray-700">Benefits</label>
                                    <input
                                        type="text"
                                        name="benefits"
                                        value={this.state.formData.benefits}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    />
                                </div>

                                <div className="mb-6">
                                    <label className="block text-gray-700">Rating</label>
                                    <div className="flex space-x-4 mt-2">
                                        {[1, 2, 3, 4, 5].map((rating) => (
                                            <label key={rating} className="inline-flex items-center">
                                                <input
                                                    type="radio"
                                                    name="rating"
                                                    value={rating}
                                                    onChange={this.handleChange}
                                                    className="form-radio"
                                                />
                                                <span className="ml-2">{rating}</span>
                                            </label>
                                        ))}
                                    </div>
                                </div>

                                <div className="mb-6">
                                    <label className="block text-gray-700">Recommendation</label>
                                    <div className="flex space-x-4 mt-2">
                                        {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((recommendation) => (
                                            <label key={recommendation} className="inline-flex items-center">
                                                <input
                                                    type="radio"
                                                    name="recommendation"
                                                    value={recommendation}
                                                    onChange={this.handleChange}
                                                    className="form-radio"
                                                />
                                                <span className="ml-2">{recommendation}</span>
                                            </label>
                                        ))}
                                    </div>
                                </div>

                                <div className="mb-6">
                                    <label className="block text-gray-700">Review</label>
                                    <textarea
                                        name="review"
                                        value={this.state.formData.review}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    />
                                </div>

                                <div className="flex justify-center">
                                    <button
                                        type="submit"
                                        className="px-6 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600"
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

function AddReviewWithNavigate(props) {
    const navigate = useNavigate();
    return <AddReview {...props} navigate={navigate} />;
}

export default AddReviewWithNavigate;
// export default AddReview;