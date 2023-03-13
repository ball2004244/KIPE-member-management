# Client-Side API Implementation

The file api.py provides a simple yet efficient way to interact with a server and perform CRUD (Create, Read, Update, Delete) operations on user and deadline data. The script includes functions for manipulating user data such as get_user(), create_user(), update_user(), and delete_user(), as well as functions for manipulating deadline data such as get_deadline(), create_deadline(), update_deadline(), and delete_deadline(). The login() function is also included for user authentication.

## Dependencies
This file relies on the following dependencies:

- requests: for sending HTTP requests to the server
- json: for parsing JSON data
- datetime: for working with dates and times
- hashing: for hashing user passwords

## Functions
### get_user(name: str) -> list
This function retrieves user data from the server based on the user's name. It sends a GET request to the server and returns a list of user objects. If the request is unsuccessful, an error message is printed.

### create_user(name: str, title: str, perm: str, dob: str, address: str)
This function creates a new user on the server. It sends a POST request with the user's name, title, permissions, date of birth, and address. If the request is successful, the function returns the user's information. If the request is unsuccessful, an error message is printed.

### update_user(id: int, name: str, title: str, perm: str, dob: str, address: str)
This function updates an existing user on the server. It sends a PUT request with the user's ID and updated information. If the request is successful, the function returns the updated user's information. If the request is unsuccessful, an error message is printed.

### delete_user(id: int)
This function deletes an existing user on the server. It sends a DELETE request with the user's ID. If the request is successful, the function returns the deleted user's information. If the request is unsuccessful, an error message is printed.

### get_deadline(date: str)
This function retrieves deadline data from the server based on the deadline date. It sends a GET request to the server and returns a list of deadline objects. If the request is unsuccessful, an error message is printed.

### create_deadline(user_id: int, name: str, deadline: str, description: str, status='Incomplete')
This function creates a new deadline on the server. It sends a POST request with the user ID, deadline name, deadline date, description, and status. If the request is successful, the function returns the deadline information. If the request is unsuccessful, an error message is printed.

### update_deadline(id: int, name: str, date: str, status: str)
This function updates an existing deadline on the server. It sends a PUT request with the deadline ID and updated information. If the request is successful, the function returns the updated deadline information. If the request is unsuccessful, an error message is printed.

### delete_deadline(id: int)
This function deletes an existing deadline on the server. It sends a DELETE request with the deadline ID. If the request is successful, the function returns the deleted deadline information. If the request is unsuccessful, an error message is printed.

### login(email: str, password:str)
This function authenticates a user on the server. It sends a POST request with the user's email and hashed password. If the request is successful, the function returns the user's information. If the request is unsuccessful, an error message is printed.

About hashed_password: The password is hashed using the SHA-256 algorithm then sent to the server for authentication.

Check out the hashing.py file for more information.

## Conclusion
The file api.py provides a useful tool for managing user and deadline data on a server. Its simple and efficient design allows for easy maintenance and scalability. With its functions for CRUD operations and user authentication, this script makes it easy to interact with the server and manage data with minimal effort.