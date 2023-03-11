import requests
import json
from datetime import datetime
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

    response = requests.post(URL, params= params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))


def update_user(id: int, name: str, title: str, perm: str, dob: str, address: str):
    data = {'id': id,
            'data':
            {'name': name, 'title': title, 'perm': perm,
                'dob': dob, 'address': address}
            }

    response = requests.put(URL, json=data)

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

def get_deadline(date: datetime.date):

    # check if the current month is already in cache 
    # if not, get the deadlines from the database
    
    try:
        with open('cache.json', 'r') as cache:
            cache_data = json.load(cache)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        cache_data = {}

    if str((date.year, date.month)) not in cache_data:
        data = {'date': date}
        response = requests.get(URL, params=data)

        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if content:
                try:
                    json_data = json.loads(content)
                except json.decoder.JSONDecodeError as e:
                    print(f'Error decoding JSON: {e}')
                    json_data = []
            else:
                json_data = []

            if not json_data:
                cache_data[str((date.year, date.month))] = [{'task_name': 'No deadlines found'}]
            else:
                cache_data[str((date.year, date.month))] = json_data

            with open('cache.json', 'w') as cache:
                json.dump(cache_data, cache)

            return cache_data[str((date.year, date.month))]
        else:
            print("Error: " + str(response.status_code))

    else:
        return cache_data[str((date.year, date.month))]

def create_deadline(name: str, date: str, status: str):
    params = {'deadline': True}
    data = {'name': name, 'date': date, 'status': status}

    response = requests.post(URL, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))


def update_deadline(id: int, name: str, date: str, status: str):
    data = {'id': id,
            'data':
            {'name': name, 'date': date, 'status': status}
            }
    
    response = requests.put(URL, json=data)
    
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


if __name__ == '__main__':
    # data = {'id': 6,
    #         'data':
    #         {'name': 'Tester', 'title': 'Tester', 'perm': 'member',
    #             'dob': '2023-02-02', 'address': 'Tester'}
    #         }
    # # create_user(data)
    # # print(update_user(data))
    # print(get_user(''))
    # print(delete_user(6))
    print(delete_deadline(3))