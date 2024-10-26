import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import NavBar from './Navbar';

class Home extends React.Component {
    add_review = () => {
        this.props.navigate('/add-review')
    }

    view_reviews = () => {
        this.props.navigate('/view-reviews')
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
                <div style={myStyle} className="opacity-40 bg-black"></div>

                {/* Main content */}
                <div className="relative z-10 flex flex-col items-center justify-center h-full text-center">
                    <h1 className="text-gray-900 text-2xl md:text-5xl font-bold mb-8 mt-20">
                        NC State Campus Jobs
                    </h1>
                    <div className="flex space-x-8 mt-20">
                        <button className="bg-red-500 hover:bg-red-200 text-white font-bold py-2 px-4 rounded-lg" onClick={() => this.add_review()}>
                            Add Reviews
                        </button>
                        <button className="bg-red-500 hover:bg-red-200 text-white font-bold py-2 px-4 rounded-lg" onClick={() => this.view_reviews()}>
                            View Reviews
                        </button>
                    </div>
                </div>
            </div>
            </div>
        );
    }
}

function HomeWithNavigate(props) {
    const navigate = useNavigate();
    return <Home {...props} navigate={navigate} />;
}

export default HomeWithNavigate;