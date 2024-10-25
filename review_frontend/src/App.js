import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Pages/Home';
import Login from './Pages/Login';
import Signup from './Pages/SignUp';
import AddReview from './Pages/AddReview';  
import Reviews from './Pages/ViewReviews'

function App() {
  return (
    <div className="App">
      <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/add-review" element={<AddReview />} />
                <Route path="/signup" element={<Signup/>}/>
                <Route path="/view-reviews" element={<Reviews/>}/>
            </Routes>
        </Router>
    </div>
  );
}

export default App;
