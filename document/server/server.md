# HTTP Server
This code implements an HTTP server that handles GET, POST, PUT, and DELETE requests. The server listens on localhost at port 8000. The server uses HTTPHandler class that extends the BaseHTTPRequestHandler class to handle incoming requests.

The storing logic is implemented in the database.py file. The database.py file contains the Database class that handles all interactions with the database.

## Dependencies
- http.server: for creating an HTTP server
- database: for interacting with a local database
- json: for serializing and deserializing JSON data

## Functionality
### GET Request
The server responds to GET requests by returning data from the database based on the query parameters. The server can return data for the following queries:

### 1.Get User by Name
Query: http://localhost:8000/?name=<name>
Response: Returns the user object for the specified name.

### 2. Get Deadline by Date
Query: http://localhost:8000/?date=<date>
Response: Returns the deadline object for the specified date.

### POST Request
The server responds to POST requests by adding data to the database. The server can add data for the following queries:

### 1. Add User
Query: http://localhost:8000/?user
Request Body: A JSON object containing user data.
Response: Returns the added user object.

### 2. Add Deadline
Query: http://localhost:8000/?deadline
Request Body: A JSON object containing deadline data.
Response: Returns the added deadline object.

### 3. Login
Query: http://localhost:8000/?login
Request Body: A JSON object containing login credentials.
Response: Returns the user object if login is successful, otherwise an error message.

### PUT Request
The server responds to PUT requests by updating data in the database. The server can update data for the following queries:

### 1. Update User
Query: None
Request Body: A JSON object containing user data with the updated fields.
Response: Returns the updated user object.

### DELETE Request
The server responds to DELETE requests by deleting data from the database. The server can delete data for the following queries:

### 1. Delete User
Query: http://localhost:8000/?user_id=<id>
Response: Returns the number of deleted users.

### 2. Delete Deadline
Query: http://localhost:8000/?task_id=<id>
Response: Returns the number of deleted deadlines.

## Conclusion
This HTTP server provides a simple API for adding, updating, and deleting data from a local database. The server can handle GET, POST, PUT, and DELETE requests and returns JSON objects in response to these requests.