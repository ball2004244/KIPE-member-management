import mysql.connector
from datetime import datetime
from auth import verify_login, hash_password

class ConnectToMySQL():
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = '12345678'
        self.port = '3306'
        self.database = 'kipe_vietnam'
        self.user_table = 'user'
        self.deadline_table = 'task'
        self.login_table = 'login'
        self.connector = None

    def connect(self) -> None:
        self.connector = mysql.connector.connect(
            host=self.host, user=self.user, password=self.password, port=self.port, database=self.database)

    def get_all_user(self):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            query = f'SELECT * FROM {self.database}.{self.user_table}'
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result

        except Exception as e:
            print('Fail to get all users from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def get_user(self, name: str):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            query = f'SELECT * FROM {self.database}.{self.user_table}'

            if name:
                name = name.strip()
                query += f' WHERE name = "{name}"'

            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

            return result

        except Exception as e:
            print('Fail to get users from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def get_user_by_id(self, id: int):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            query = f'SELECT * FROM {self.database}.{self.user_table}'

            if id:
                query += f' WHERE user_id = {id}'

            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

            return result

        except Exception as e:
            print('Fail to get users from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def get_user_by_email(self, email):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            query = f'''SELECT u.user_id, u.title, u.perm, u.address, 
                        u.dob, u.name, l.email
                        FROM user u
                        JOIN login l ON u.user_id = l.user_id
                        WHERE l.email = '{email}';'''

            cursor.execute(query)
            result = cursor.fetchall()[0]

            cursor.close()

            return result

        except Exception as e:
            print('Fail to get users from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def add_user(self, data: dict):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            name = data['name']
            title = data['title']
            perm = data['perm']
            dob = data['dob']
            address = data['address']
            # get latest id

            query = f'SELECT MAX(user_id) FROM {self.user_table}'
            cursor.execute(query)
            id = list(cursor.fetchone().values())[0]

            if not id:
                id = 1
            else:
                id += 1

            # add data to database

            query = f'INSERT INTO {self.database}.{self.user_table} (user_id, name, title, perm, dob, address) VALUES (%s, %s, %s, %s, %s, %s)'
            values = (id, name, title, perm, dob, address)
            cursor.execute(query, values)

            self.connector.commit()
            cursor.close()

            return {'status': 'success', 'message': 'Added user successfully'}

        except Exception as e:
            print('Fail to create user')
            print(e)
            return {'status': 'fail', 'message': 'Fail to add user'}

        finally:
            if self.connector:
                self.connector.close()

    def delete_user(self, id: int):
        try:
            self.connect()
            cursor = self.connector.cursor()

            query = f"DELETE FROM {self.database}.{self.user_table} WHERE user_id = '{int(id)}'"
            cursor.execute(query)

            self.connector.commit()
            cursor.close()
            return {'status': 'success', 'message': 'Deleted user successfully'}

        except Exception as e:
            print('Fail to delete user')
            print(e)
            return {'status': 'fail', 'message': 'Failed to delete user'}

        finally:
            if self.connector:
                self.connector.close()

    def update_user(self, new_data: dict):
        try:
            self.connect()
            cursor = self.connector.cursor()
            id = new_data['id']
            name = new_data['name']
            title = new_data['title']
            perm = new_data['perm']
            dob = new_data['dob']
            address = new_data['address']

            query = f'''UPDATE {self.database}.{self.user_table}
                        SET name = "{name}",
                            title = "{title}",
                            perm = "{perm}",
                            dob = "{dob}",
                            address = "{address}"
                        WHERE user_id = {id}'''
            
            cursor.execute(query)

            self.connector.commit()
            cursor.close()
            return {'status': 'success', 'message': 'User updated successfully'}

        except Exception as e:
            print('Fail to update user')
            print(e)
            return {'status': 'fail', 'message': 'Fail to update user'}

        finally:
            if self.connector:
                self.connector.close()

    def get_deadline(self, deadline: str):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            query = f'SELECT * FROM {self.database}.{self.deadline_table}'

            if deadline:
                query += f' WHERE deadline = "{deadline}"'

            cursor.execute(query)
            result = cursor.fetchall()

            # modify result so that it can be used in frontend
            # convert datetime to string
            result = [dict((k, v.strftime('%Y-%m-%d') if isinstance(v, datetime) else v) for k, v in d.items()) for d in result]
            cursor.close()

            return result

        except Exception as e:
            print('Fail to get deadline from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def get_deadline_for_user(self, uid: int, deadline: str):
        try: 
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            query = f'SELECT * FROM {self.database}.{self.deadline_table} WHERE user_id = {uid}'

            if deadline:
                query += f' AND deadline = "{deadline}"'

            cursor.execute(query)
            result = cursor.fetchall()

            # modify result so that it can be used in frontend
            # convert datetime to string
            result = [dict((k, v.strftime('%Y-%m-%d') if isinstance(v, datetime) else v) for k, v in d.items()) for d in result]
            cursor.close()

            return result
        except Exception as e:
            print('Fail to get deadline from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def add_deadline(self, data: dict):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            uid = data['uid']
            name = data['name']
            deadline = data['deadline']
            status = data['status']
            description = data['description']
            
            # get latest id

            query = f'SELECT MAX(task_id) FROM {self.deadline_table}'
            cursor.execute(query)
            id = list(cursor.fetchone().values())[0]

            if not id:
                id = 1
            else:
                id += 1

            # add data to database

            query = f'INSERT INTO {self.database}.{self.deadline_table} (task_id, user_id, task_name, deadline, status, description) VALUES (%s, %s, %s, %s, %s, %s)'
            values = (id, uid, name, deadline, status, description)
            cursor.execute(query, values)

            self.connector.commit()
            cursor.close()

            return {'status': 'success', 'message': 'Added deadline successfully'}

        except Exception as e:
            print('Fail to create deadline')
            print(e)
            return {'status': 'fail', 'message': 'Fail to add deadline'}

        finally:
            if self.connector:
                self.connector.close()

    def delete_deadline(self, id: int):
        try:
            self.connect()
            cursor = self.connector.cursor()

            query = f"DELETE FROM {self.database}.{self.deadline_table} WHERE task_id = '{int(id)}'"

            cursor.execute(query)

            self.connector.commit()
            cursor.close()
            return {'status': 'success', 'message': 'Deleted deadline successfully'}

        except Exception as e:
            print('Fail to delete deadline')
            print(e)
            return {'status': 'fail', 'message': 'Failed to delete deadline'}

        finally:
            if self.connector:
                self.connector.close()

    def update_deadline(self, new_data: dict):
        try:
            self.connect()
            cursor = self.connector.cursor()
            task_id = new_data['task_id']
            user_id = new_data['uid']
            name = new_data['name']
            deadline = new_data['deadline']
            status = new_data['status']
            description = new_data['description']

            query = f'''UPDATE {self.database}.{self.deadline_table}
                        SET task_name = "{name}",
                            user_id = "{user_id}",
                            deadline = "{deadline}",
                            status = "{status}",
                            description = "{description}"
                        WHERE task_id = {task_id}'''
            
            cursor.execute(query)

            self.connector.commit()
            cursor.close()
            return {'status': 'success', 'message': 'Deadline updated successfully'}

        except Exception as e:
            print('Fail to update deadline')
            print(e)
            return {'status': 'fail', 'message': 'Fail to update deadline'}

        finally:
            if self.connector:
                self.connector.close()

    def get_login_detail(self, data: dict):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            email = data['email']
            password = data['password']

            query = f'SELECT * FROM {self.database}.{self.login_table} WHERE email = "{email}"'

            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()

            if not result:
                return {'status': 'fail', 'message': 'Invalid email'}
            elif not verify_login(password, self.get_password(email)):
                return {'status': 'fail', 'message': 'Invalid password'}

            result = self.get_user_by_email(email)
            result['status'] = 'success'
            # return {'status': 'success', 'message': 'Login successfully'}
            return result

        except Exception as e:
            print('Fail to get login detail')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def get_password(self, email):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            query = f"SELECT password FROM {self.database}.{self.login_table} WHERE email = '{email}'"
            cursor.execute(query)
            result = cursor.fetchone()['password']
            cursor.close()

            return result

        except Exception as e:
            print('Fail to get user')
            print(e)
            return {'status': 'fail', 'message': 'Fail to get password'}

        finally:
            if self.connector:
                self.connector.close()

    def add_login_user(self, user_id: int, email: str, password: str):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            # get latest id

            query = f'SELECT MAX(login_id) FROM {self.database}.{self.login_table}'
            cursor.execute(query)

            id = list(cursor.fetchone().values())[0]

            if not id:
                id = 1
            else:
                id += 1

            # add data to database
            query = f'INSERT INTO {self.database}.{self.login_table} (login_id, user_id, email, password) VALUES (%s, %s, %s, %s)'
            cursor.execute(query, (id, user_id, email, password))
            self.connector.commit()

            cursor.close()

            return {'status': 'success', 'message': 'Added user successfully'}

        except Exception as e:
            print('Fail to create user')
            print(e)
            return {'status': 'fail', 'message': 'Fail to add user'}

        finally:
            if self.connector:
                self.connector.close()


database = ConnectToMySQL()


if __name__ == '__main__':
    '''
            name = data['name']
            title = data['title']
            perm = data['perm']
            dob = data['dob']
            address = data['address']
    '''
    # user = {'name':'Testing', 'title':'Testing', 'perm':'member', 'dob':'2023-01-01', 'address':'Testing'}
    # database.add_user(user)
    # database.update(2, {2, 'Retest', 'Retest', 'member', '2023-02-01', 'Retest'})
    # result = database.get_all_user()
    # print(result)
    # deadline = database.get_deadline('2021-08-01')
    # print(deadline)

    # database.add_login_user(100, 'test', hash_password('12345678'))
    database.add_login_user(110, 'testmem', hash_password('12345678'))
