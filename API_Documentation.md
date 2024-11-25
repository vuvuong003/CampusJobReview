## Authentication

### 1. Obtain JWT Token

- **URL**: `/auth/token/`
- **Method**: `POST`
- **Description**: This endpoint triggers the `MyTokenObtainPairView` to handle user authentication and returns a JWT token upon successful login.
- **Request Body**:
  ```json
  {
    "username": "username",
    "password": "password"
  }
  ```
- **Returns**:
  ```json
  {
    "status": 200,
    "data": {
      "val": true,
      "tokens": {
        "access": "access_token",
        "refresh": "refresh_token"
      }
    }
  }
  ```
  - `400 Bad Request`: If the credentials are invalid.

### 2. Refresh JWT Token

- **URL**: `/auth/token/refresh/`
- **Method**: `POST`
- **Description**: This endpoint uses `TokenRefreshView` to refresh the access token using the refresh token.
- **Request Body**:
  ```json
  {
    "refresh": "refresh_token"
  }
  ```
- **Returns**:
  ```json
  {
    "status": 200,
    "access": "new_access_token"
  }
  ```
  - `400 Bad Request`: If the refresh token is invalid or expired.

### 3. User Registration

- **URL**: `/auth/register/`
- **Method**: `POST`
- **Description**: This endpoint triggers the `RegisterView` to handle user registration and returns a success message if registration is successful.
- **Request Body**:
  ```json
  {
    "username": "new_username",
    "email": "newuser@example.com",
    "password": "password"
  }
  ```
- **Returns**:
  ```json
  {
    "status": 200,
    "data": {
      "val": true,
      "detail": "Registration Successful. Please verify your email"
    }
  }
  ```
  - `400 Bad Request`: If the username already exists or if there are validation errors.

---

## Email verification

**URL**: /auth/verify-email/<uidb64>/<token>/
**Method**: `GET`
**Description**: This endpoint triggers the VerifyEmailView to handle email verification.
**Returns**:

```json
{
  "status": 200,
  "message": "Email verified successfully."
}

or

{
  "status": 400,
  "message": "Invalid verification link."
}
```

## Profile Section

### 1. Get Profile

**URL**: `/auth/profile/`
**Method**: `GET`
**Description**: This endpoint triggers the ProfileView to retrieve the authenticated user's profile information.
**Returns**:

```json
{
  "username": "testuser",
  "email": "testuser@example.com",
  "first_name": "Test",
  "last_name": "User",
  "bio": "This is a test bio."
}
```

## 2. Update Profile

**URL**: `/auth/profile/`
**Method**: `PUT`
**Description**: This endpoint triggers the ProfileView to update the authenticated user's profile information.
**Request body**:

```json
{
  "first_name": "Updated",
  "last_name": "User",
  "bio": "Updated bio."
}
```

**Returns**:

```json
{
  "username": "testuser",
  "email": "testuser@example.com",
  "first_name": "Updated",
  "last_name": "User",
  "bio": "Updated bio."
}
```

## Reviews

### 1. Create Review

- **URL**: `/reviews/`
- **Method**: `POST`
- **Description**: Allows authenticated users to create a new review.
- **Request Body**:
  ```json
  {
    "department": "Sales",
    "job_title": "Sales Associate",
    "hourly_pay": 15.5,
    "review": "Great place to work",
    "rating": 5,
    "locations": "New York"
  }
  ```
- **Returns**:
  ```json
  {
    "status": 201,
    "data": {
      "id": 1,
      "department": "Sales",
      "job_title": "Sales Associate",
      "hourly_pay": 15.5,
      "review": "Great place to work",
      "rating": 5,
      "locations": "New York",
      "reviewed_by": "username"
    }
  }
  ```
  - `400 Bad Request`: If validation fails.

### 2. Filter Reviews

- **URL**: `/filter/`
- **Method**: `GET`
- **Description**: Filters reviews based on parameters like `department`, `locations`, `job_title`, `min_rating`, and `max_rating`.
- **Query Parameters**:
  - `department`: Filter by department name.
  - `locations`: Filter by location.
  - `job_title`: Filter by job title.
  - `min_rating`: Minimum rating.
  - `max_rating`: Maximum rating.
- **Returns**:
  ```json
  [
    {
      "id": 1,
      "department": "Sales",
      "job_title": "Sales Associate",
      "hourly_pay": 15.5,
      "review": "Great place to work",
      "rating": 5,
      "locations": "New York",
      "reviewed_by": "username"
    }
  ]
  ```
  - `200 OK`: List of filtered reviews.

---

## Vacancies

### 1. Create Vacancy

- **URL**: `/vacancies/`
- **Method**: `POST`
- **Description**: Allows authenticated users to create a new vacancy.
- **Request Body**:
  ```json
  {
    "jobTitle": "Sales Associate",
    "jobDescription": "Responsible for assisting customers",
    "maxHoursAllowed": 40
  }
  ```
- **Returns**:
  ```json
  {
    "status": 201,
    "data": {
      "id": 1,
      "jobTitle": "Sales Associate",
      "jobDescription": "Responsible for assisting customers",
      "maxHoursAllowed": 40
    }
  }
  ```
  - `400 Bad Request`: If validation fails.

## Comments

### 1. Create Comment

- **URL**: `/comments/<review_id>/`
- **Method**: `POST`
- **Description**: Allows authenticated users to create a comment under a job review.
- **Request Body**:
  ```json
  {
    "created_at": "2024-11-25T06:36:59.069241Z",
    "id": 30,
    "review": 7,
    "text": "good review",
    "user": "vhv123"
  }
  ```
- **Returns**:
  ```json
  {
    "status": 201,
    "data": {
      "id": 30,
      "review": 7,
      "user": "vhv123",
      "text": "good review",
      "created_at": "2024-11-25T06:36:59.069241Z"
    }
  }
  ```
  - `400 Bad Request`: If validation fails.

### 2. Delete Comment

- **URL**: `/comments/<review_id>/<id>/`
- **Method**: `DELETE`
- **Description**: Allows authenticated users to delete a comment by its ID
- **Path Parameter**: id (integer): The ID of the comment to delete
- **Returns**:
  ```json
  {
    "status": 204,
    "message": "Comment deleted successfully."
  }
  ```
  - `404 Not Found`: If the comment does not exist
  - `403 Forbidden`: If the user is not authorized to delete the comment
