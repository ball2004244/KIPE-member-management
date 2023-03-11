import mysql.connector
from datetime import datetime
# Communicate with database


class ConnectToMySQL():
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = '12345678'
        self.port = '3306'
        self.database = 'kipe_vietnam'
        self.user_table = 'user'
        self.deadline_table = 'task'
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

    def get_user(self, name=None):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            query = f'SELECT * FROM {self.database}.{self.user_table}'

            if name:
                name = name.strip()
                query += f' WHERE name LIKE "{name}%"'

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
            data = new_data['data']
            set_values = ', '.join(
                [f"{key} = '{val}'" for key, val in data.items()])

            query = f"UPDATE {self.database}.{self.user_table} SET {set_values} WHERE user_id = {id}"
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

    def get_deadline(self, date):
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            date += ' 00:00:00'
            try:
                date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                print('Fail to convert date')
                print(e)
                date = datetime.strptime('1990-2-2 00:00:00', '%Y-%m-%d %H:%M:%S')
            
            
            query = f'SELECT * FROM {self.database}.{self.deadline_table} WHERE YEAR(deadline) = {date.year} AND MONTH(deadline) = {date.month}'

            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result

        except Exception as e:
            print('Fail to get deadlines from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def add_deadline(self, data: dict):
        pass 

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

                

database = ConnectToMySQL()

if __name__ == '__main__':
    '''
            name = data['name']
            title = data['title']
            perm = data['perm']
            dob = data['dob']
            address = data['address']
    '''
    user = {'name':'Testing', 'title':'Testing', 'perm':'member', 'dob':'2023-01-01', 'address':'Testing'}
    database.add_user(user)
    # database.update(2, {2, 'Retest', 'Retest', 'member', '2023-02-01', 'Retest'})
    # result = database.get_all_user()
    # print(result)
    # deadline = database.get_deadline('2021-08-01')
    # print(deadline)

