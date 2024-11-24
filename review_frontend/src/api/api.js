/**
 * @fileoverview Utility module for making API calls to the backend services
 * Contains both protected (authenticated) and unprotected API calling functions
 * @module api-service
 */

/**
 * Base URL for the API endpoints
 * @constant {string}
 */
export let base_url = "http://localhost:8000/";

export let frontend_url = "http://localhost:3000/";

/**
 * URL endpoint for user authentication
 * @constant {string}
 */
export let login_url = base_url + "auth/token/";

/**
 * URL endpoint for sending otp to user email
 * @constant {string}
 */
export let send_otp_url = base_url + "auth/send-otp/"

/**
 * URL endpoing for updating password of an existing user
 * @constant {string}
 */
export let update_password_url = base_url + "auth/update-password/"

/**
 * URL endpoint for user registration
 * @constant {string}
 */
export let register_url = base_url + "auth/register/";

/**
 * URL endpoint for service reviews
 * @constant {string}
 */
export let review_url = base_url + "service/reviews/";

/**
 * URL endpoint for filtering services
 * @constant {string}
 */
export let filter_url = base_url + "service/filter";

/**
 * Makes an API call that doesn't require authentication
 * @async
 * @param {string} url - The endpoint URL to make the request to
 * @param {Object} [data={}] - The data to send with the request
 * @param {string} [type="POST"] - The HTTP method to use (GET, POST, etc.)
 * @returns {Promise<Response>} The fetch response object
 * @throws {Error} Logs error and shows alert on server error
 */
export let unprotected_api_call = async (url, data = {}, type = "POST") => {
  try {
    // Initialize headers with content type and ngrok skip
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("ngrok-skip-browser-warning", true);

    let requestOptions = {
      method: type,
      headers: myHeaders,
      redirect: "follow",
    };

    // Configure request options based on HTTP method
    if (type !== "GET") {
      requestOptions.body = JSON.stringify(data);
    }

    const response = await fetch(url, requestOptions);
    return response;
  } catch (error) {
    console.log("API Error:", error);
    throw error;
  }
};

/**
 * Makes an API call that requires authentication token
 * @async
 * @param {string} url - The endpoint URL to make the request to
 * @param {Object} [data={}] - The data to send with the request
 * @param {string} [type="POST"] - The HTTP method to use (GET, POST, etc.)
 * @returns {Promise<Response>} The fetch response object
 * @throws {Error} Logs error and shows alert on server error
 */
export let protected_api_call = async (url, data = {}, type = "POST") => {
  try {
    // Retrieve and parse authentication token from localStorage
    let token = localStorage.getItem("user_data");
    token = JSON.parse(token)["data"]["tokens"]["access"];

    // Initialize headers with authentication token
    var myHeaders = new Headers();
    myHeaders.append("Authorization", "Bearer " + token);
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("ngrok-skip-browser-warning", true);

    let raw;
    let requestOptions;

    // Configure request options based on HTTP method
    if (type === "GET") {
      requestOptions = {
        method: "GET",
        redirect: "follow",
        headers: myHeaders,
      };
    } else {
      // For non-GET requests, stringify the data and include in body
      raw = JSON.stringify(data);
      requestOptions = {
        method: type,
        headers: myHeaders,
        body: raw,
        redirect: "follow",
      };
    }

    let response = await fetch(url, requestOptions);
    console.log(response);
    return response;
  } catch (e) {
    console.log(e);
    alert("Server Error");
  }
};
