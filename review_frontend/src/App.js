/**
 * @fileoverview Main application component with routing configuration
 * Sets up the primary routing structure for the NC State Campus Jobs Review application
 */

import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Pages/Home";
import Login from "./Pages/Login";
import Signup from "./Pages/SignUp";
import AddReview from "./Pages/AddReview";
import Reviews from "./Pages/ViewReviews";

/**
 * @function App
 * @description Root component of the application that sets up routing
 * @returns {JSX.Element} The rendered application with route configuration
 *
 * Routes:
 * - / : Home page
 * - /login : User authentication
 * - /add-review : Create new job review (requires authentication)
 * - /signup : New user registration
 * - /view-reviews : Browse and filter job reviews
 */
function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          {/* Landing page route */}
          <Route path="/" element={<Home />} />

          {/* Authentication routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          {/* Review management routes */}
          <Route path="/add-review" element={<AddReview />} />
          <Route path="/view-reviews" element={<Reviews />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
