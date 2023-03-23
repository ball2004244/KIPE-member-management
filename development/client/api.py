import requests
from hashing import hash_password
URL = "http://localhost:8000"

'''MANIPULATING USERS'''

def get_user(name: str) -> list:
    data = {'name': name}

    response = requests.get(URL, params=data)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error: " + str(response.status_code))


def create_user(name: str, title: str, perm: str, dob: str, address: str):
    params = {'user': True}
    data = {'name': name, 'title': title, 'perm': perm,
            'dob': dob, 'address': address}

    response = requests.post(URL, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))


def update_user(id: int, name: str, title: str, perm: str, dob: str, address: str):
    params = {'user': True}
    data = {'id': id, 'name': name, 'title': title, 'perm': perm,
            'dob': dob, 'address': address}

    response = requests.put(URL, params=params, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))


def delete_user(id: int):
    data = {'user_id': id}
    response = requests.delete(URL, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))


'''MANIPULATING DEADLINES'''


def get_deadline(date: str):

    # check if the current month is already in cache
    # if not, get the deadlines from the database

    # try:
    #     with open('cache.json', 'r') as cache:
    #         cache_data = json.load(cache)
    # except (FileNotFoundError, json.decoder.JSONDecodeError):
    #     cache_data = {}
    data = {'date': date}
    response = requests.get(URL, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))

def get_deadline_for_user(user_id: int, date: str):
    data = {'date': date, 'uid': user_id}
    response = requests.get(URL, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))

def create_deadline(user_id: int, name: str, deadline: str, description: str, status='Incomplete'):
    params = {'deadline': True}
    data = {'uid': user_id, 'name': name, 'deadline': deadline,
            'status': status, 'description': description}

    response = requests.post(URL, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))


def update_deadline(task_id: int, user_id: int, name: str, deadline: str, status: str, description: str):
    params = {'task': True}
    data = {'task_id': task_id, 'uid': user_id, 'name': name, 'deadline': deadline,
            'status': status, 'description': description}

    response = requests.put(URL, params=params, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))


def delete_deadline(id: int):
    data = {'task_id': id}
    response = requests.delete(URL, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))


'''LOGIN LOGIC'''


def login(email: str, password: str):
    params = {'login': True}
    data = {'email': email, 'password': hash_password(password)}
    response = requests.post(URL, params=params, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))

'''UPLOAD IMAGE'''
def upload_avatar(user_id: int, avatar_path: str):
    params = {'avatar': True}

    # send the image to the server
    headers = {'Content-Type': 'multipart/form-data'}

    # read the binary data from the file object
    with open(avatar_path, 'rb') as file:
        data = file.read()

    # encode the data as a multipart form-data request
    files = {'avatar': (f'{user_id}.jpg', data, 'image/jpeg')}

    # send the request
    response = requests.post(URL, headers=headers, files=files)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))

if __name__ == '__main__':
    # data = {'id': 6,
    #         'data':
    #         {'name': 'Tester', 'title': 'Tester', 'perm': 'member',
    #             'dob': '2023-02-02', 'address': 'Tester'}
    #         }
    # # create_user(data)
    # # print(update_user(data))
    # print(get_user('Retest'))
    # print(delete_user(6))
    # create_deadline(5, 'Test', '2021-02-02', 'Test')
    # print(get_deadline('2021-02-02'))
    # print(update_deadline(4, 5, 'Test', '2021-02-02', 'Complete', 'Test'))
    print(upload_avatar(5, r'C:\Users\nguye\Downloads\kipe_logo.jpg'))
