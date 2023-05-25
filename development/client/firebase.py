import os
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred, {
        'storageBucket': '' # Firebase URL
    })

def upload_image(name: str, image: bytes):
    # upload the image to firebase storage
    bucket = storage.bucket()
    blob = bucket.blob(name)
    blob.upload_from_file(image)

    return 'Upload successfully'

def get_image(name):
    # get the avatar url from firebase storage
    path = './Resource/avatar.jpg'
    bucket = storage.bucket()
    blob = bucket.blob(name)
    blob.download_to_filename(path)
    return path

if __name__ == '__main__':
    print(upload_image('1.jpg',r'C:\Users\nguye\Downloads\kipe_logo.jpg'))






