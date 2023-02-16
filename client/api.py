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
    data = {'name': name, 'title': title, 'perm': perm,
            'dob': dob, 'address': address}

    response = requests.post(URL, json=data)
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
    data = json.dumps(id)
    response = requests.delete(URL, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code))


'''MANIPULATING DEADLINES'''

def get_deadline(date: datetime.date):
    # formatted_date = datetime.strptime(date, r'%Y-%m-%d')
    # print(formatted_date)
    data = {'date': date}
    response = requests.get(URL, params=data)

    if response.status_code == 200:
        if not response.json():
            return ['No deadlines found']
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
    data = json.dumps(id)
    response = requests.delete(URL, json=data)

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
    print(get_deadline('2021-08-01'))