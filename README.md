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

The site uses a minimalistic colour scheme to project the brand's image.
The four main colours are red, white, grey and black. Various shades of these colours are used to highlight certain pieces of information or to denote an interactive element such as a button/link.

Red and white are intrinsic to the brand's image as they are the colours of an 'L' plate which learner drivers have to display on their cars.

### Layout

The site's layout is intuitive and accessible.
It has been designed with a mobile-first approach to responsive web design and follows the conventions of good practice.

Bootstrap has been used to create the framework for the site's layout.
It provides a built in grid structure with responsive breakpoints. 
Alongside the Bootstrap grid, custom CSS and media queries optimise the user experience for mobile users.

Navigation elements are positioned at the top of the page for ease of access from any page.

The footer which contains copyright information is fixed to the very bottom of each page.

Headings and subheadings are of appropriate size level to denote level of importance and separate information into blocks. Each page contains a header to display to the user which page they are on.

Large pieces of information such as a user's lessons are displayed to them in a table.
By using this layout, the desired information is easily retrieved and digested.

Images are of good resolution and appropriate file size. They resize responsively across all screen sizes and are relevant to the information they support.


### Navigation

The navbar is simple, it features the brand logo and the brand's name which link to the home page. If the user is signed in, it also displays a profile icon with a dropdown menu. If a user has added their name to their profile, their initials are displayed in the icon. Otherwise a default user icon is displayed. The dropdown menu has links to book a lesson, the user's profile, the lessons they've booked as well as the sign out link.
The idea behind using a dropdown with the user's profile icon is that the site and its features are all centered around the user, all dropdown options are links to user initiated events a learner driver will want to carry out such as booking a lesson, viewing the details of their lessons or updating their profile.

![navbar](docs/screenshots/navbar.png)


![navbar dropdown](docs/screenshots/navbar-dropdown.png)

The profile page uses Bootstrap nav tabs. This allows for quick and easy flicking between the profile page and the lessons page. Similarly, the lessons page uses tabs to sort the view of lessons by upcoming and previous.

![profile nav tabs](docs/screenshots/profile-nav-tabs.png)

![profile nav tabs](docs/screenshots/lessons-nav-tabs.png)

Links and buttons...

Buttons are styled using the Bootstrap 'btn' class with subclasses of 'btn-lg', 'btn-sm' and a custom class 'btn-xs'. Buttons are coloured using the Bootstrap 'btn-danger' or 'btn-dark' class as well as custom colour styling.

Links have hover attributes applied to change colour which indicate to the user it's an interactive element.


# Features

## User Authentication

All user authentication occurs via Django-Allauth. The base allauth templates have been customised with additional CSS including layout adjustments, colour scheme, brand name and logo.

### Register

![Sign Up Page](/docs/screenshots/register.png)

User feedback is provided in the form of a Bootstrap alert if registration was successful.

### Sign In

![Sign In Page](/docs/screenshots/sign-in.png)

User feedback is provided in the form of a Bootstrap alert if sign in was successful.

![Sign In Success Alert](/docs/screenshots/sign-in-alert.png)

### Sign Out

![Sign Out Page](/docs/screenshots/sign-out.png)

User feedback is provided in the form of a Bootstrap alert if sign out was successful.

![Sign Out Success Alert](/docs/screenshots/sign-out-alert.png)

### Forgotten Password
BUG- No email will be sent as email backend not set up! User will have to get in contact and admin will have to manually reset it.

![Forgotten Password]()

## Home Page

The home page features a large hero image alongside text with a 'scroll' style animation applied via CSS and JavaScript.

The home page default for an anonymous user (not signed in):
![Home Page for Anonymous User](docs/screenshots/home.png)

The home page for an authenticated user (signed in):
![Home Page for Authenticated User](docs/screenshots/home-authorised.png)

## User Profile

### Profile Page

If a user has not completed all parts of their profile, a Bootstrap toast message will appear giving them a todo list. The list will tell the user which parts of their profile are missing.

![Incomplete Profile](docs/screenshots/profile-incomplete.png)

Otherwise if their profile is complete, users can edit their details by clicking on the red pen icons which trigger a modal containing a form for them to fill out the new details.

![Profile Completed](docs/screenshots/profile-complete.png)

The myLessons Upcoming section displays the 5 soonest bookings the user has made. If a user has bookings it will look like this:

![Upcoming Lessons](docs/screenshots/upcoming-lessons.png)

Each booking is displayed as a Bootstrap list item and is a link. When clicked it will take the user to the invoice for that lesson.

### myLessons Page

The myLessons page is split into tabs, this allows for viewing lesson data based on lesson date and time. It has a section to view all lessons, upcoming lessons and previous lessons.

#### All Lessons Tab

If a user hasn't booked any lessons yet, they'll be greeted with this message alongside a button linking to the booking page.
![No Lessons Booked](/docs/screenshots/lessons-no-lessons-booked.png)


If they have made a booking, the bookings are displayed in a table format sorted by soonest lesson date and time.The booking reference is a link which allows the user to view the invoice for that lesson at any time.

![All Lessons](docs/screenshots/all-lessons.png)

If the user has previous bookings, the booking will display in the table alongside a previous icon and the table row will have the Bootstrap 'table-secondary' class applied making it greyed out.

![Previous Icon](docs/screenshots/previous-icon.png)

If the user has cancelled their lesson, the lesson is still available to view for their reference but will display a red 'CANCELLED' stamp alongside the booking. The table row will have the Bootstrap 'table-danger' class applied making it red.
The stamp has JavaScript applied to randomly rotate the stamp at an angle for each instance of the class. This makes it look like a person has stamped it on.

![Cancelled Stamp](docs/screenshots/cancelled-stamp.png)


#### Coming Up Lessons Tab

The Coming Up tab pane displays all bookings that are in the future, sorted by soonest lesson date and time.

![Coming Up](docs/screenshots/coming-up.png)


#### Previous Lessons Tab

If a user doesn't have any previous lessons, the previous tab pane will display like so:
![Previous No Previous Bookings](docs/screenshots/previous.png)

Otherwise, the previous tab pane displays all bookings that are in the past. Sorted in reverse order so the oldest lesson will be at the bottom.

![Previous](docs/screenshots/previous-2.png)

#### Invoice Page
The site does not provide booking confirmations via email. Instead, proof of booking is provided in an invoice that is available to access by clicking the booking reference link for the lesson on the lessons page.

![Invoice]()

## Booking System

The booking system is split up into multiple parts. For each part, when the user presses 'Continue' the form data is collected and saved to session storage to be displayed and inserted into the booking form on the checkout page.
The progress bar and disabled nav tabs at the top of the page help the user identify how far along the booking process they are. The progress bar is animated indicating that the process is active and open, awaiting their input. Upon successful checkout, the progress bar is a 100% width static red, indicating they are done.

### 1. Lesson Type Selection

The first part of the booking process is the lesson type selection page. Here users can select a lesson type, either for a manual or automatic car or a mock driving test from the dropdown menu.

![Lesson Type Selection](docs/screenshots/booking-1.png)

![Lesson Type Dropdown](docs/screenshots/lesson-type-dropdown.png)

### 2. Lesson Meeting Point Address Input

Here, the user can enter the address for where they'd like their instructor to meet them and pick them up.

**FUTURE FEATURE*: Since a user needs a full home address to make a booking, there should be a checkbox for them to select if they want meeting at their home address. The user's home address could be retrieved from their user profile and inserted into the form via JavaScript.

![Lesson Meeting Point Address Input](docs/screenshots/booking-2.png)

### 3. Lesson Date Selection

Here, users can choose from any of the available dates in the dropdown selection.
A Python function queries the Booking model in the database to find all dates in the next 30 days (starting from tomorrow) that are not fully booked and appends them to the list.

When the user clicks 'Continue', the lesson date selected is saved to session storage to be used to calculate which times are available.

![Lesson Date Selection](docs/screenshots/booking-3.png)

![Lesson Date Dropdown](docs/screenshots/lesson-date-dropdown.png)

### 4. Lesson Time Selection

Here, the user can choose a time from the dropdown selection. The times displayed are calculated by a Python function which queries the database for times not already booked on the date selected by the user.

![Lesson Time Selection](docs/screenshots/booking-4.png)

![Lesson Time Dropdown](docs/screenshots/lesson-time-dropdown.png)


### 5. Checkout
The checkout page features a form where users will submit their billing and payment details. To the right of the form the user's lesson details are displayed for their reference, if they wish to amend their booking before paying, they can quit, leave the checkout and go back. Their own personal details are also included here, this is so that the user can check their contact details are up to date before booking.

![Checkout Page](docs/screenshots/checkout.png)

While Stripe is handling the payment, a red overlay with a spinning arrow is displayed blocking off the user's controls until the payment has been processed.

![Checkout Overlay](docs/screenshots/checkout-overlay.png)

### 6. Checkout Success/Booking Confirmed
The Checkout success page displays after booking and payment were successful. It is displayed via a unique URL which takes the booking reference number as a parameter. An green 'success' alert is displayed to the user upon successful checkout.

The success page displays an invoice for the user to go over the details of their booking.

![Checkout Success/Booking Confirmed Page](docs/screenshots/success.png)



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
