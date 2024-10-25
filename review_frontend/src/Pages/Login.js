import * as React from 'react';
import NavBar from './Navbar';
import { useNavigate } from 'react-router-dom';

class Login extends React.Component {

    state = {
        formData: {
            email: "",
            password: ""
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
                            Login
                        </h1>
                        <div className="bg-white w-[40vw] h-[40vh] shadow-lg flex items-center justify-center p-10 overflow-y-auto">
                            <form onSubmit={this.handleSubmit}>
                                <div className="mb-6">
                                    <label className="block text-gray-700">Email</label>
                                    <input
                                        type="text"
                                        name="email"
                                        value={this.state.formData.email}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    />
                                </div>

                                <div className="mb-6">
                                    <label className="block text-gray-700">Password</label>
                                    <input
                                        type="text"
                                        name="password"
                                        value={this.state.formData.password}
                                        password={true}
                                        onChange={this.handleChange}
                                        className="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    />
                                </div>

                                <div className="flex justify-center">
                                    <button
                                        type="submit"
                                        className="px-6 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600"
                                    >
                                        Login
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

function LoginWithNavigate(props) {
    const navigate = useNavigate();
    return <Login {...props} navigate={navigate} />;
}

export default LoginWithNavigate;