# NC STATE JOBS RATING AND REVIEW SYSTEM 

The original authors of this project are 
- [Mohit Soni](https://github.com/mohitsoni2111)
- [Tilak Satra](https://github.com/tilaksatra)
- [Akshat Savla](https://github.com/akshat22)
- [Madiha Mansoori](https://github.com/madiha2001)
- [Anagha Patil](https://github.com/Anagha-2000)

Please refer to the original repository [here!](https://github.com/akshat22/campus-job-review-system)

To gain a deeper understanding of the changes and improvements from the original project to the newly enhanced version, please watch the demo video. This video showcases the new functionalities and highlights the enhancements made throughout the project

## Table of contents

- [Introduction](#Introduction)
- [Demo Video](#demo-video)
- [Newly Enhanced Features](#newly-enhanced-features)
- [Future Scope](#future-scope)
- [Installation](#installation)
- [Licence](#License)
- [Contributions](#contributions)
- [CODE-OF-CONDUCT](#CODE-OF-CONDUCT)
- [Technology Stack](#technology-stack)
- [Team Members](#team-members)
- [Documentation](#documentation)

### Introduction
Are you considering an on-campus job but unsure what to expect? Or have you worked or are currently working in one and want to share your experience to help your peers in their job search?

Our newly enhanced Campus Job Review System is a one-stop destination for students seeking answers about on-campus jobs. This comprehensive platform empowers students by allowing them to upload and explore reviews of various job opportunities. Built with Django and MongoDB, the system benefits from Django's rapid development capabilities and MongoDB's flexibility in managing diverse review data.

After visiting our website, students will leave with a fresh perspective, reassured that their questions have been addressed. By leveraging insights from peers who have firsthand experience, they can make informed decisions about their on-campus employment options.

Explore our platform and take the first step towards finding the right on-campus job for you!


[![DOI](https://zenodo.org/badge/876539766.svg)](https://doi.org/10.5281/zenodo.14007974)
![Python Badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)                             ![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=white)      ![MongoDB](https://img.shields.io/badge/MongoDB-brightgreen?logo=mongodb&logoColor=white)       ![Django](https://img.shields.io/badge/Django-darkgreen?logo=django&logoColor=white)        ![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

[![Autopep8 Check](https://github.com/SAT510/CampusJobReview/actions/workflows/autopep.yml/badge.svg)](https://github.com/SAT510/CampusJobReview/actions/workflows/autopep.yml)     [![Pylint Check](https://github.com/SAT510/CampusJobReview/actions/workflows/pylint.yml/badge.svg)](https://github.com/SAT510/CampusJobReview/actions/workflows/pylint.yml)     [![Black](https://github.com/SAT510/CampusJobReview/actions/workflows/black.yml/badge.svg)](https://github.com/SAT510/CampusJobReview/actions/workflows/black.yml) [![Prettier](https://github.com/SAT510/CampusJobReview/actions/workflows/prettier.yml/badge.svg)](https://github.com/SAT510/CampusJobReview/actions/workflows/prettier.yml) 

[![GitHub open issues](https://img.shields.io/github/issues-raw/SAT510/CampusJobReview)](https://github.com/SAT510/CampusJobReview/issues?q=is%3Aopen)  
[![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/SAT510/CampusJobReview)](https://github.com/SAT510/CampusJobReview/issues?q=is%3Aclosed)

[![Django Tests](https://github.com/SAT510/CampusJobReview/actions/workflows/django-tests.yml/badge.svg)](https://github.com/SAT510/CampusJobReview/actions/workflows/django-tests.yml)  [![Jest Tests](https://github.com/SAT510/CampusJobReview/actions/workflows/jest_tests.yml/badge.svg)](https://github.com/SAT510/CampusJobReview/actions/workflows/jest_tests.yml)   

[![codecov](https://codecov.io/gh/SAT510/CampusJobReview/graph/badge.svg?token=3U8KLQ8AA4)](https://codecov.io/gh/SAT510/CampusJobReview)

<p align="center"><img width="700" src="./resources/Intro_to_CampusJobReview.gif"></p>

### Animation Video About Project 
[Click Here to Watch the Video!](https://drive.google.com/file/d/1cmAgHYnGPp1LA3F_dimup3XeC6HHNplY/view?usp=sharing)


### Demo Video 
Explore a demo of our application [here!](https://drive.google.com/file/d/1u1iyAw3LeA0d42yTTJDXIi-HXPxxlzvG/view?usp=sharing)

### Newly Enhanced Features
We have made lots of changes to ensure that our app is feasible, maintainable, extendable, and can be used by a broad audience. Throughout this process, we have extended various features and fixed bugs. Our enhancements and bug fixes include:

1. Database Migration: We have migrated the current minimal SQL to MongoDB. This ensures enhanced performance, particularly with faster queries for dynamic filtering, while also improving scalability.

2. Frontend Upgrade: We migrated from foundational HTML/CSS to React for a more dynamic and responsive user experience, providing a seamless, real-time interface that better meets user needs.

3. Security Enhancements: We have implemented secure login and sign-up processes by improving authentication mechanisms through JWT tokenization, which allows for secure access to job reviews and user data.

4. Browser Extension: We have integrated a browser API with the cloud MongoDB database to allow for job review pop-ups and form autofill when viewing or applying for jobs, minimizing repetitive data entry and enhancing job search ease.

5. Enhanced User Interaction: We added dynamic filters for pay rate, ratings, job locations, and more, allowing users to sort various fields for a more focused and personalized approach to their job searches.

6. Backend upgrade: Upgraded to a django rest framework from a basic flask application. This allows portability of the application.

### Future Scope
1. Form Validation: Enhance frontend form validaition to have stronger checks and better user experience.

2. Browser Extension Enhancement: Extend the browser extension to be integrated with the backend and show the complete review. Additionally, add an auto-fill feature based on the review information that would simplify data entry, enhancing user-friendliness and efficiency.

3. Community Features: Introduce a forum or discussion board where users can share experiences, ask questions, and provide advice on job applications and interviews. This could foster a community around job hunting and reviews.

4. Mobile Application Development: Develop a mobile version of the CampusJobReview platform to allow users to access job listings, submit reviews, and receive notifications on the go, enhancing accessibility and user engagement.

### Installation
For detailed installation steps tailored to your operating system, please refer to the [INSTALL.md](https://github.com/SAT510/CampusJobReview/blob/test/INSTALL.md) file. This guide aims to provide you comprehensive instructions as to how to set up and run your project smoothly, regardless of whether you are using Windows or macOS. We highly recommend that you follow the steps in a chronological manner to ensure a successful installation. 

### License
This project is licensed under the Apache License. For further details, please refer to the [License](https://github.com/SAT510/CampusJobReview/blob/test/LICENSE.md).

### Contributions 
We invite you to check our [CONTRIBUTING.md](https://github.com/SAT510/CampusJobReview/blob/project-resources/CONTRIBUTING.md) for guidelines on contributing to the repository and helping us enhance the project. We encourage and apprecite collaboration and would love to hear new ideas and any suggestions. We appreciate all types of collaboration whether you are a developer, a designer, or someone wih new ideas. Join our community and help us make this project even better for everyone! 

### CODE-OF-CONDUCT
We encourage any contributions, but please make sure that these steps are taken in a respectful manner,in accordance with our [CODE-OF-CONDUCT](https://github.com/SAT510/CampusJobReview/blob/test/CODE-OF-CONDUCT.md). We strive to make this project a good experience for everyone and we value an inclusive environment as a paramount in our project. 

### Technology Stack
- <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" width="120"/>

- <img src="https://img.shields.io/badge/Django-darkgreen?logo=django&logoColor=white" alt="Django" width="120"/>

- <img src="https://img.shields.io/badge/MongoDB-brightgreen?logo=mongodb&logoColor=white" alt="MongoDB" width="120"/>

- <img src="https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=white" alt="React" width="120"/>

### Documentation
Explore our methodologies in developing the Campus Job Review application through this comprehensive guide.

1. Use Case Mini Tutorial: Discover the enhanced features of the application by following along with engaging use cases illustrated through various images. [Click here to get started!](https://github.com/SAT510/CampusJobReview/blob/shazia_testing/UseCase_Documentation.md)

2. Add API Endpoints and give brief description. [Click here to get started!](https://github.com/SAT510/CampusJobReview/blob/test/API_Documentation.md)

  
4. Outline of the development and specifications of the CampusJobReview project including technical details, project goals, architecture, feature implementations, and potential areas for future development. This document includes the point description of all the classes and methods of the system. [SystemSpecDoc](https://github.com/SAT510/CampusJobReview/blob/test/project_docs/CSC-510.pdf)

### Team Members
- Amay Gada
  - ahgada@ncsu.edu
- Tahreem Yasir
  - tyasir@ncsu.edu
- Shazia Muckram 
  - smuckra@ncsu.edu

Feel free to reach out to us for any questions or concerns. We are happy to help and would love to meet you all!
