# Contents

1. [Milestone Project 4](#milestone-project-4)

    i. [Assessment Criteria](docs/assessment_criteria.pdf)

    ii. [Project Brief](#project-brief)
    
    iii. [Main Technologies](#main-technologies)

2. [About](#about)

3. [Design Phase](#design-phase)

4. [UX](#ux)

    i. [Application Goals](#application-goals)

    ii. [User Stories](#user-stories)

5. [UI](#ui)

    i. [Design Choices](#design-choices)

    ii. [Wireframes](#wireframes)

    iii. [Site Map](#site-map)

6. [Application Features](#application-features)

7. [Accessibility](#accessibility)
    
    i. [Google Lighthouse](#google-lighthouse)

8. [Version Control](#version-control)

    i. [Git & GitHub](#git--github)

9. [Debugging](#debugging)

    i. [Error Handling](#error-handling)

10. [Testing](#testing)

    i. [Test Environment](#test-environment)

    ii. [Manual Testing](#manual-testing)

    iii. [Automated Testing](#automated-testing)

    iv. [Code Validation](#code-validation)

11. [Deployment](#deployment)

    i. [ElephantSQL](#elephantsql)
    ii. [Amazon Web Services (AWS)](#amazon-web-services-aws)
    iii. [Heroku](#heroku)

12. [References & Acknowledgements](#references--acknowledgements)

    i. [Code](#code)

    ii. [Media](#media)

    iii. [Icons](#icons)

    iv. [Fonts](#fonts)


## Milestone Project 4
This project is my submission for Milestone Project 4: Full Stack Frameworks with Django. The final project for the Level 5 Diploma in Web Applications Development.

### [Assessment Criteria](docs/assessment_criteria.pdf)

### Project Brief

1. Django Full Stack Project

    - Build a Django project backend by a relational database to create a website that allows users to store and manipulate data about a particular domain. 

2. Multiple Apps

    - The project must be a brand new Django project, composed of multiple apps (an app for each potentially reusable component in the project).

3. Data Modelling

    - Put some effort into designing a relational database schema well-suited for the domain. Make sure to put some thought into the relationships between entities. Create at least two custom Django models beyond the examples shown on the course. 

4. User Authentication

    - The project should include an authentication mechanism, allowing a user to register and log in. There should be a good reason as to why the user would need to do so.

5. User Interaction

    - Include at least one form with validation that will allow users to create and edit models in the back-end (in addition to the authentication mechanism).

6. Use of Stripe

     - At least one of the Django apps should contain some e-commerce functionality using Stripe. This may be a shopping cart checkout or single payments. After paying successfully, the user would gain access to additional functionality/content on the site. Not that for this project, Stripe's test functionality should be used, rather than actual live payments.

7. Structure and Navigation

    - Incorporate a main navigation menu and structured layout. This could be achieved using Bootstrap, for example.

8. Use of JavaScript

    - The front-end should contain some JavaScript logic which enhances the user experience.

9. Documentation

    - Write a README.md file that explains what the project does and the value it provides to its users.

10. Version Control

    - Use Git and GitHub for version control.

11. Attribution

    - Maintain a clear separation between code written by oneself and code from external sources. Attribute any code from external sources to its source via comments above the code or for larger dependencies, in the README.

12. Deployment

    - Deploy the final version to a hosting platform such as Heroku.

13. Security

    - Make sure not to include any passwords or secret keys in the project repository. Make sure to turn off the Django DEBUG mode which could expose secrets.


### Technologies Used

#### Languages

- HTML
- CSS
- JavaScript
- Python

#### Frameworks

- Django 3.2 (LTS Version)
- Bootstrap 5

#### Libraries

- jQuery
- Bootstrap 5
- FontAwesome Icons
- Google Fonts

#### APIs

- Amazon Web Services (AWS)
- S3 Bucket
- Google Sheets API

#### Data & Databases

- JSON
- SQLite
- PostgreSQL
- ElephantSQL

#### Security & Authentication

- Django Allauth
- IAM (AWS & Google)
- Google OAUTH 2.0

#### Version Control & Deployment

- Git
- GitHub
- Heroku


# About

This website is for "Jim's School of Motoring" a fictional driving school which uses it's online platform to manage learner driver's lesson bookings and collect payments.

The site is centered around user profile functionality. In this way, it provides an online portal allowing learners to register for an account to be able to book their lessons online. When a user books a lesson, they can view the details at any time from their profile.
User profiles can be updated at any time by editing individual personal details such as address, telephone number etc. This ensures details associated with the booking are up to date.

The booking process queries the database to only display the dates and times that are available (not already booked) and will save the user's booking to the database if their payment details are validated by Stripe and the payment is successful.


# Design Phase

## UX

### Site Goals

#### 1. Booking System

Design, develop and deploy a booking system which is effective in taking learners' bookings.

- Collect the learners' details from their user profile.

    - The booking system will need to query the user's profile to retrieve this data and assign it to the booking so that each booking is associated with the user who made it.

        - The idea behind this approach is that it will save the user time if they only have to fill out their details once when initialising their profile instead of manually inputting it in the form each time they want to book a lesson.

    - These details must already be populated fields in the database before a booking can be made, therefore appropriate error handling and user feedback to prompt the user to complete their profile needs implementing if that is not the case.

- Display a selection of dates and times that are available to book.

    - The booking system will need to query the booking database model to only display dates and times that have not already been booked.These will need to be displayed to the user for selection in an intuitive and easy to read format.

        - Dates will need to be displayed having been reformatted from the SQL database datefield: 'MM/DD/YYYY' (e.g. 02/22/2024) to 'd, DD/MM/YYYY' (e.g. Thurs, 22/02/2024) since this site is aimed at users in the UK.

        - The user selection needs to be easy to navigate and to select the desired date and time. This could be developed using either a select dropdown displaying only the available dates and times or even a datepicker with the unavailable date/time options disabled.

- Save and store user's selection prior to payment and booking creation.

    - The user's selection will need to be stored somewhere to be accessed upon checkout and prior to booking creation.
    This data should be posted to and stored in the Django session storage until the user decides to checkout. Upon successful checkout, the booking system form will collect the user's selection and delete it from session storage.


- Price Model
    - Create a separate model for the lesson price.
        - The price model will include a unique decimal field for staff/admin to edit and update the lesson price should they need to.
        - Only one instance of lesson price is allowed.
            - Lesson prices can be edited and updated by those with permission but further instances can not be created.
    
    - The price field in the Booking model needs to be a foreignkey object of the Price model. This ensures any booking made will have the updated price charged to it.
        

- Take payment via Stripe

    - Payments for bookings will be taken via Stripe's API.

    - A payment intent will need to be created for each payment and assigned a unique client ID. For staff/admin reference, the payment intent id will be saved to the booking to allow for quick and easy querying inside Django admin or Stripe Dashboard.
    From Stripe dashboard, payments can be viewed, amended and refunded.

    - Make use of secure Stripe Webhook functionality to mitigate user/server error to prevent mischarges, fraud attempts and diagnose faults in the payment and data collection process.


- Booking Creation

    - The booking form will need to be validated to ensure the data it collects is in the format the database is expecting to receive and is valid and no essential data is null. If not valid, appropriate error handling and user feedback must be implemented and payments must not be taken without a booking being made.

    - The booking model should automatically generate a UUID booking reference for each instance created. It should also auto-add the date and time the booking was made.

- Checkout Success Page

    - Upon successful checkout and booking creation, the user should be redirected to a confirmation/success page.
    - This page should display all the details of their booking.


#### 2. User Profiles

Design, develop and deploy unique user profiles for each user who registers an account with the site.

- Create a User Profile database model
    - The user profile model must contain a one to one field of 'user' from the Django User model. This ensures that the user profile instance is associated with the account they set up.

- Upon site registration, when accessing their profile from the navbar, users will be prompted to complete their profile. This can be done via alerts, toasts or flash messages. A todo list might prove helpful to give user feedback about which parts of the profile need completing.

- User CRUD (Create, Read, Update, Delete) functionality.
    - Users must be in control of their data and interactions at all times.
    - Users must be able to read any data associated with their profile in an easily accessible and intuitive manner.
    - Users must be able to create profiles (or have a blank one set up automatically upon registration).
    - Users must be able to update their profile if they need to make amendments to their personal details such as telephone number or home address.
    - Users must be given the option to delete their profiles and site accounts should they want. They need to be in control of their personal data, who has access to it and be able to revoke it at any time without impediment. 


- The user profile page will display the user's lessons if they have booked them.
    - Lessons must be displayed in an intuitive and easily digestible format. This could be a table.
    - Users should be able to sort how they view the data such as viewing lessons by date and time, upcoming or previous.


#### 3. Home Page

- The home page must immediately tell a new user what the site is for and what the business is about.
- It should include promotional material to advertise the services the business is providing.
    - Detailed list of services and prices etc.
    - Images to support information.
- Contact information should be included on the home page.

#### 4. User Authentication

- Prior to making any changes to the database, users must be authenticated. Django-Allauth will handle user authentication via email/username and password. A user that is not signed in must not be able to change data associated with bookings or user profiles.


### User Stories

#### As a user, I want to be able to...

- Immediately see the purpose of this site and the value it can provide me.
- Quickly get the contact details for the business.
- Understand the services and prices on offer.
- Understand what area the business is based in.
- Register for an account.
    - Log in and out securely.
    - Change my password if I forget it.
    - Delete my account when I want.
- Update and delete my user profile as I wish.
- Book lessons online in just a few clicks and checkout securely.
    - Receive confirmation that my booking was successful.
- View all the lessons I have booked and easily see the details.
    - Sort viewing of my lessons by date and time such as upcoming/previous or cancelled lessons.

- Amend my lesson booking.
- Cancel my lesson booking.

#### As a member of staff/the site admin, I want to be able to...
- Manage bookings in the admin panel.
    - Take bookings and payment directly such as over the phone via card details/bank transfer and add the booking details to the database.
    - Take bookings and payment via the site's booking system and Stripe.
    - Create bookings.
    - Update bookings.
    - Cancel bookings. Keeping the booking in the database but assigning the cancelled value True.
    - Delete bookings.

    - View all upcoming bookings in a spreadsheet or calendar which should automatically update whenever changes are made in the database.

- Manage any payments made via Stripe in the Stripe Dashboard.
    - Take payment.
    - View payment.
    - Amend payment.
    - Refund payment.

- Adjust the price of lessons if I need to.
    - Whenever I adjust the lesson price, any bookings made from that point on should be charged the updated price.

- Manage user profiles in the admin panel.
    - Add user details.
    - View user details.
    - Update user details.
    - Delete user details.

# UI

## Wireframes

### Home Page
#### Anonymous User:

![Home Page for Anonymous User](/docs/wireframes/home_anon.jpg)

#### Authenticated User:

![Home Page for Authenticated User](/docs/wireframes/home_auth.jpg)


### User Profile Page

![User Profile Page](/docs/wireframes/profile.jpg)

### myLessons Page

![myLessons Page](/docs/wireframes/lessons.jpg)

### Booking System

#### 1. Select Lesson Type

![Booking System- Select Lesson Type](/docs/wireframes/booking_1.jpg)

#### 2. Select Lesson Date

![Booking System- Select Lesson Date](/docs/wireframes/booking_2.jpg)

#### 3. Select Lesson Time

![Booking System- Select Lesson Time](/docs/wireframes/booking_3.jpg)

#### 4. Enter Meeting Point Address

![Booking System- Select Lesson Meeting Point Address](/docs/wireframes/booking_4.jpg)

#### 5. Checkout Page

![Booking System- Checkout Page](/docs/wireframes/checkout.jpg)

#### 6. Checkout Success Page

![Booking System- Checkout Success](/docs/wireframes/success.jpg)



## Design Choices

### Colour Scheme

### Layout

### Navigation

- Navbar Dropdown

- Nav Tabs on Profile


# Features

## User Authentication
## Register
## Sign In
## Sign Out
## Forgotten Password

## User Profile Page

### Profile

### myLessons


## Booking System





# Version Control

## Git & GitHub

# Testing

## Code Validation

### HTML5 Validation

### CSS3 Validation

### Python3 PEP8 Compliance

### JavaScript Linting


# Deployment
<!-- Document Deployment Procedure -->

## ElephantSQL
<!-- Document database setup -->

## Amazon Web Services (AWS)
<!-- Document AWS S3 Bucket Setup -->

## Heroku
<!-- Document value of using Heroku -->

# References & Acknowledgements

## Code

## Media

### Images

## Icons

### Font Awesome Icons

## Fonts

### Google Fonts
