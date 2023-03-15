# Client-Side GUI Design

## Overview
This file provide a guideline for every aspects about GUI. This is mostly implemented from the file gui_design.py on the client side. The client-side application enables users to log in and access different screens based on their permissions. The application includes the following screens:

1. Login Screen
2. Home Screen
3. Screen for Managing Deadlines (HR/Admin only)
4. Screen for Managing Members (HR/Admin only)

## Dependencies

- sys, os: interacting with files and directories 
- datetime: working with dates and times
- functools: creating partial functions
- PyQt5.uic, PyQt5.QtGui, PyQt5.QtWidgets, PyQt5.QtCore: creating GUIs
- api: interacting with a backend server. 

## Login Screen
The login screen is implemented using the LoginScreen class and allows users to log in with their email and password. The screen includes the following features:

- Input fields for email and password
- Button for submitting login information
- Error handling for missing or invalid input
- Navigation to the home screen upon successful login

## Home Screen
The home screen is implemented using the HomeScreen class and displays information based on the user's permissions. The screen includes the following features:

- User avatar and information
- Links to external resources
- Navigation to the deadline and member management screens
- Logout button

### Member Home Screen
If the user is a member, the home screen displays their tasks and a calendar.

### HR/Admin Home Screen
If the user is an HR or admin user, the home screen displays options for managing deadlines and members.

## Managing Deadlines Screen
The managing deadlines screen is implemented using the ManageDeadlineScreen class and allows users to create, update, and delete deadlines. It is linked to the HR Home Screen. The screen includes the following features:

- Input fields for deadline information
- Buttons for creating, updating, and deleting deadlines
- Calendar for selecting deadlines to view
- List of deadlines for the selected date
- Error handling for missing or invalid input

### AddDeadline Dialog
This is the pop-up dialog that appears when hr clicks the `Add Deadline` button. It allows hr to create a new deadline by typing in the task name, member's id, and description.

### ModifyDeadline Dialog
This is the pop-up dialog that appears when hr clicks any of the task appears under the calendar. It allows hr to modify the deadline information, as well as delete deadline.

## Managing Members Screen
The managing members screen is implemented using the ManageMemberScreen class and allows HR and admin users to create, update, and delete member information. It is linked to the HR Home Screen. The screen includes the following features:

- Input fields for member information
- Buttons for creating, updating, and deleting members
- Search bar for finding members
- List of members based on search results
- Error handling for missing or invalid input

## Conclusion
This client-side application provides a simple and user-friendly interface for managing deadlines and member information. With its intuitive navigation and error handling, users can efficiently perform their tasks and stay on top of their responsibilities.