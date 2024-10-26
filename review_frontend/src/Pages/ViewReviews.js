import * as React from 'react';
import NavBar from './Navbar';
import { useNavigate } from 'react-router-dom';


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
        jobs: [
          {
            jobTitle: 'Gym Trainer',
            jobDescription: 'Supervise the students in the gym',
            department: 'NC State Gym',
            location: 'Carmichael Gym',
            hourlyPay: '$12.75',
            benefits: 'None',
            review: 'Good Job',
            rating: 5,
            recommendation: 9,
            reviewedBy: 'asavla',
          },
          {
            jobTitle: 'Student Worker',
            jobDescription: 'Makes Sandwiches',
            department: "Jason's Deli",
            location: 'Talley Student Union',
            hourlyPay: '$10',
            benefits: 'Employee meals',
            review: 'Manager not friendly',
            rating: 4,
            recommendation: 7,
            reviewedBy: 'asavla',
          },
          {
            jobTitle: 'Student Worker',
            jobDescription: 'Cashier, Server Line',
            department: 'NC State Dining',
            location: 'Fountain Dining Hall',
            hourlyPay: '$10',
            benefits: 'Employee meals',
            review: '6 hour shifts get hectic',
            rating: 4,
            recommendation: 8,
            reviewedBy: 'asavla',
          },
          {
            jobTitle: 'Barista',
            jobDescription: 'Make coffees',
            department: 'Port City Java',
            location: 'EB-2',
            hourlyPay: '$10',
            benefits: 'Employee meals',
            review: 'Great environment',
            rating: 5,
            recommendation: 10,
            reviewedBy: 'mmansoori',
          },
        ],
      };

    handleChange = (e) => {
        this.setState({
            formData: {
                ...this.state.formData,
                [e.target.name]: e.target.value,
            },
        })
    };

    handleSubmit = (e) => {}
    
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
                            Reviews
                        </h1>
                        <div className="bg-white w-[95vw] h-[40vh] shadow-lg flex items-center justify-center p-10 overflow-y-auto">
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
                                        jobTitle={job.jobTitle}
                                        jobDescription={job.jobDescription}
                                        department={job.department}
                                        location={job.location}
                                        hourlyPay={job.hourlyPay}
                                        benefits={job.benefits}
                                        review={job.review}
                                        rating={job.rating}
                                        recommendation={job.recommendation}
                                        reviewedBy={job.reviewedBy}
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