# Use Case Mini Tutorial 

## Welcome to a mini tutorial of our Campus Job Review web application. Here, you will get a detailed view about what to expect in the application, explore the various enhanced features and new functionalities, and look at real-life examples of using the application through screenshots. 

### Landing Page
As you enter our application, you will be greeted by a beautiful home page that truly represents the wolfpack spirit of NCSU. Here you will find various tabs such as the Home, Login, and Signup. You will also see an Add Reviews and a View Reviews Button. 

![Landing-Page](docs/images/landing_page.jpeg)

### Authentication 
The first step as you start your journey of exploring the Campus Job Review web application is to sign up using a username and password. Make sure that your password includes letters and numbers which will make sure that you have the right requirements to sign up successfully. 

#### Sign Up
The picture below shows the page that opens up when you click the SIGNUP button that is located on the top right corner of the landing page. 
![SignUp-Landing-Page](docs/images/sign_up.png)

Once you are here, choose a strong username and password to sign up yourself to start using the application. Then, click on the Sign Up button in blue. 
![SignUp-Details-Page](docs/images/sign_up_fill.png)

**Successful Registration**: 
Once you have met the requirements for the username and password, you will see a pop-up indicating a successful registration. It will then tell you to visit the email that you entered to verify email address.
![SignUp-Success-Page](docs/images/sign_up_success.png)

- **Verify Email**:
You will receive an email from the application. Click on the link provided to verify your email address and proceed to the log in process
![Verify-Email](docs/images/verify_email.png)

**Failed Registration**: 
 Given that a username or email already exists, you will not be able to sign up and will recieve a unsuccessful message. Other cases where you will not be able register successfully include not entering a username or leaving the password empty. An example of a failed registration can be seen in the picture below. 
![SignUp-Failure-Page](docs/images/sign_up_fail.png)

#### Login
Now that you have successfully signed up as a valid user, let us login to the application. You can click on the LOGIN button located at the top right corner which sits in between the HOME and the SIGNUP buttons. Once you click LOGIN, you will be greeted with the following page: 
![Login-landing-Page](docs/images/login_landing.png)

   It is time to login with the same credentials that you used to sign up. Enter the details and your page will look similar to the image below. 
    ![Login-details-Page](docs/images/login_details.png)
**Successful Login**: Given that you have entered a valid username and password based on the details that you used to signup, you will be directed to a new page with new buttoms. The new options available can be seen at the top right corner as "ADD REVIEW", "VIEW REVIEWS", "PROFILE", and "LOGOUT".
![Login-success-Page](docs/images/login_success.png)
**Failed Login**: Given that you have entered the incorrect username or password, you will see a pop-up explaining that you have entered the invalid credentials. Time to try again!
![Login-failure-Page](docs/images/login_fail.png)
    - **Reset Password**: In case you cannot login and do not remember your password, you may click on the "Reset Password?" button at the bottom and it will redirect you to this page. You will need to enter your email address and click on "Send OTP"
    ![Forgot-Password](docs/images/forgot_pass.png)
    - Once successfully enter a valid email address, you will be directed to a new page requesting a one-time password with a time limit of 10 minutes.
    ![Enter-OPT](docs/images/enter_otp.png)
    - You will need to check your email for the OTP. You will a 6 digit number in bold. That will be the one-time password you need to reset the password. This is what the email should look like.
    ![Reset-Password-Email](docs/images/reset_pass_email.png)
    - You will enter the 6 digit number into the text field. If you incorrectly enter the OTP, you will see a pop up explaining that your OTP is incorrect. You will need to try again
    ![Wrong-OTP](docs/images/wrong_otp.png)
    - Once you correctly entered the OTP, you will be directed to the reset password page, where you will enter a new password and confirm it.
    ![Reset-Password](docs/images/reset_password.png)
    - Once you successfully enter a valid password and confirmed it, you will see a pop up notifying you that your passsword is successfully changed and redirect you to the login page.
    ![Reset-Password](docs/images/reset_password_success.png)

### Add Review
We offer the option for you to add a review to help your peers make informed decisions about the on-campus jobs. You are required to fill in various fields which include Job Title, Department, Location, Job Description, Hourly Pay, Benefits, Rating, Recommendation, and Review. 

The following is an example of the page that you will encounter when you click on the Add Review Button. 
The following image is an example of a valid review with all the fields filled accurately and as expected. 
![Add_review-filled-Page](docs/images/add_review_filled.png)

- Successful completion: Once you have entered all the details without missing any fields, click on the "Submit your review" button at the bottom of the page. Then, you will see a pop-up indicating that you were able to sucessfully add you review. 
![Add_review-filled-Page](docs/images/add_review_success.png)

- Failed in Adding a Review: Given that you don't fill all the fields that are required in the review form, you will encounter a pop-up telling you that there was an error in submitting your review. This will require you to verify your review again.

    The following image shows an example of a an error when adding a review: 
    ![Add_review-failure-Page](docs/images/add_review_failure.png)


### View Reviews 
When you click on the View Reviews button, you should be able to see the job reviews that were added by your peers and by you. For each job review, you will be able to see the job title and the hourly pay.

The page should look similar to the following: 
![View_Review_Landing-Page](docs/images/view_reviews_landing.png)

- For each job review, you may click on the job title name or the expand button as it will expand the section elaborating on the experiences and details about an on-campus job. These details include the review along with the person reviewed it as well as the description, department, location, employee benefits and the recommendation rating. At the bottom is the comments section which allows any user to interact with the reviewer by asking questions, providing tips or simply make a comment on the job review!
![Expand-Job-Review](docs/images/expand_job_review.png)

### Discussion Forum
To add a comment to a job review, simply type in your comment and hit the "Post Comment" button. Here is an example of what your page might look like.
![Post-Comment](docs/images/post_comment.png)

After you posted your comment, it will be visible by everyone. This is what your page might look like. To delete a comment, simply hit the trash can by the comment you want to delete and it will be removed in the comments section.
![View-Comment](docs/images/view_comment.png)


### Filter Reviews
We offer an exclusive and easy option for you to filter the reviews based on fields such as Department, Location, and Job Title. Moreover, we also allow you to set a filter on reviews based on the minimum and maximum ratings by your peers. This makes it easier for you to locate the most useful pieces of information in no time. To reset the filters, simply hit the "Reset Button" and all the filters will be resetted. Below is an example of filtering the reviews based on the department.
    ![Filter_reviews_page](docs/images/filter_reviews.png)

### Browser Extension
With the integration of a browser API, users will experience enhanced functionality:

Job Review Pop-Ups: When browsing job postings, you will receive pop-ups through our browser extension that currently show the title of the job based on the department title that is associated with the list of reviews on our website. Below are the pictures showing the browser extension functionality. 
![Browser_Extension_page](docs/images/browser_extension_1.jpg)
![Browser_Extension2_page](docs/images/browser_extension_2.jpg)


### Logout
Once you have explored all the reviews or added reviews, you can log out while making sure that all your changes are saved. This adds another layer of security measure. Click on the LOGOUT option located on the top right corner and you will be directed back to the landing page as shown below. 
![Landing-Page](docs/images/landing_page.jpeg)
