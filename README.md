# KIPE Member Management System
## Description
This is the Member Management System developed by @ball2004244, aimed to provide effcient managing program for HR Department at KIPE Vietnam. Our website is hosted at kipevietnam.com, please feel free to check it out.

About this program, it is the client-server system that enable information transfer with low latency (< 20ms) and high security (using complex algorithms and various security methodologies). 

About the server, I may host it using the same domain of KIPE's website. 

About the client, it is a desktop application which gives different permissions to the user based on their accounts. The user can only login through a provided account to gain access to the application, and all the other ways of gaining access without admin's permission would be considered illegal. 

For more detail into the technical aspect, please take a look at the section below.

## Please read all file in the document directory to get the general idea of this program
All the documents are located at document folder, including:
1. client folder:
- GUI.md: the description for client-side user interface.
- api.md: contains description for client-side back-end logic.

2. server folder:
- server.py: contains details about our HTTP server, which used to receive and response to requests from the clients.
- database.py: contains all information about the process of communicating with MySQL database.

## How to run this program?
Currently, the system can be run in two different ways:

### In development settings
To run the system in development mode, please follow these steps:
1. Enable the virtual environment by addressing the activate file at venv/Scripts/activate
2. Even though all the dependencies are pre-installed, you can reinstall them in case any error occur. The information about dependencies are mentioned in each documents, and also in the file requirements.txt
3. Run the file server/server.py using python. The message "Server is running at port 8000" will pop up means that the server is running properly.
4. Run the file client/gui_design.py using python. A desktop window will pop up if there is no error. 
5. Play around with the client-side features, and take a look at the console on both client and server-side.

### In production settings
To run the system in production mode, please follow these steps:
1. Enable the virtual environment by addressing the activate file at venv/Scripts/activate
2. The server is already hosted at http://kipevietnam.com/hr_server, so you don't need to run the server file. However, you can still check it out in the production folder. 
3. Run the file production/client/gui_design.py using python. This is a configurated application that connect to the online server.

## Current Development Progress
Version 1.0.0: 03/14/2023
- Initialize connection to online server
- Finish login logic
- HR can view all members' information, search for specific members, and add/delete members. Remaining task: Edit member information.
- HR can interact with the built-in calendar to view and add new deadlines. Remaining task: Edit/delete deadlines.
- Member can view their deadlines by interacting with the calendar. Remaining task: Fetch real deadlines from the server.

What may come up in the next version:
- HR can edit member information and edit/delete deadlines.
- Member can see real deadlines from the server.
- Member can set their own avatar and title.
- The hyperlink will function properly.

Version 1.0.1: 03/21/2023 (estimated)
- Finished edit/delete deadlines
- Finished update member information
- Hyperlink navigates to right page
- Member can see real deadlines from the server
- Working on Avatar and Title