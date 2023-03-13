# ConnectToMySQL Class Documentation
## Description
The ConnectToMySQL class provides methods to interact with a MySQL database. 

## Dependencies
- mysql.connector: connect to a MySQL database. 
- datetime: working with date and time.
- auth: working with authentication.

## Attributes
- host: Database host address (default 127.0.0.1)
- user: Database user
- password: Database password
- port: Database port (default 3306)
- database: Database name
- user_table, deadline_table, login_table: Name of several tables in the database
- connector: MySQL connector object

## Methods
### connect(): 
a method that connects to the MySQL server using the mysql.connector.connect() method and sets the connector attribute to the resulting connection.

### GET Request
### 1. get_all_user(): 
a method that retrieves all user data from the user table in the database and returns it as a list of dictionaries.

### 2. get_user(name: str): 
a method that retrieves user data from the user table in the database based on the given name parameter, which is a string representing the name of the user to retrieve. It returns the matching user data as a list of dictionaries.

### 3. get_user(id: int): 
a method that retrieves user data from the user table in the database based on the given id parameter, which is an integer representing the ID of the user to retrieve. It returns the matching user data as a list of dictionaries.

### 4. get_user_by_email(email): 
a method that retrieves user data from the user and login tables in the database based on the given email parameter, which is a string representing the email address of the user to retrieve. It returns the matching user data as a dictionary.

### 5. get_deadline(deadline: str): 
a method that retrieves task data from the task table in the database based on the given deadline parameter, which is a string representing the deadline of the task(s) to retrieve. If deadline is not provided, it retrieves all task data from the table. It returns a list of dictionaries containing the task data, with date values converted to strings for compatibility with frontend display.

### 6. get_login_detail(self, data: dict): 
This method retrieves the login details of a user from the database. It takes a dictionary as input that contains the following keys: email and password.

### 7. get_password(self, email): 
This method retrieves the password of a user from the database. It takes an email address as input.

### PUT Request
### 1. add_user(data: dict): 
a method that adds a new user to the user table in the database based on the given data parameter, which is a dictionary containing the user's name, title, perm, dob, and address. It generates a new user_id for the user based on the latest user_id in the table, and inserts the new user data into the table. It returns a dictionary with a status key indicating whether the operation was successful and a message key with a corresponding message.

### 2. add_deadline(self, data: dict): 
a method that adds a new deadline to the database. It takes a dictionary as input that contains the following keys: uid, name, deadline, status, and description.

### 3. add_login_user(self, user_id: int, email: str, password: str): 
a method that adds a new login account to the database. It takes an integer ID, an email address, and a password as input.

### DELETE Request
### 1. delete_user(id: int): 
a method that deletes a user from the user table in the database based on the given id parameter, which is an integer representing the ID of the user to delete. It deletes the user data from the table and returns a dictionary with a status key indicating whether the operation was successful and a message key with a corresponding message.

### 2. delete_deadline(self, id: int): 
This method deletes a deadline from the database. It takes an integer ID as input that corresponds to the ID of the deadline to be deleted.

### UPDATE Request
### 1. update_user(new_data: dict): a
method that updates a user's data in the user table in the database based on the given new_data parameter, which is a dictionary containing the user's id and the new data to update. It constructs an SQL query to update the user's data in the table and returns a dictionary with a status key indicating whether the operation was successful and a message key with a corresponding message.

### 2. update_deadline(self, data: dict): 
This method updates a deadline in the database. It takes a dictionary as input that contains the following keys: id, uid, name, deadline, status, and description. 
THIS IS CURRENTLY UNDER CONSTRUCTION!!!

## Conclusion
The ConnectToMySQL class provides a set of methods to interact with a MySQL database. The class requires mysql.connector, datetime, and auth as dependencies. The class has several attributes including host, user, password, port, database, user_table, deadline_table, login_table, and connector. The methods are categorized into GET, PUT, DELETE, and UPDATE requests. These methods allow retrieval, addition, deletion, and updating of user and deadline data from the atabase. There are several functions that are currently under construction.