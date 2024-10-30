# API Documentation

The Campus Job Review system provides many API products, tools, and resources that enable you to read first-hand reviews from those who have worked on campus and add your own reviews.


## Base URL
`http://127.0.0.1:8000/` 

## Authentication Endpoints 

### 1. Obtain JWT Token 
- **URL**: /auth/token/
- **Method**: POST
- **Description**: This endpoint triggers the MyTokenObtainPairView to handle user authentication and returns a JWT token upon successful login.
- **Request Body**:
 ```json
  {
    "username": "username",
    "password": "aaaa1234"
  }
  TO DO

### 2. Refresh JWT TOKEN
