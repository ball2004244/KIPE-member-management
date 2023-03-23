import os
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred, {
        'storageBucket': 'kipe-management.appspot.com'
    })

#  upload image to firebase storage
def upload_to_firebase_storage(name, image):
    # the current image is a binary retrieved from the HTTP server
    # we need to save it to a file first
    with open(name, 'wb') as f:
        f.write(image)

    # upload the image to firebase storage
    bucket = storage.bucket()
    blob = bucket.blob(name)
    blob.upload_from_filename(name)
    return blob.public_url



if __name__ == '__main__':
    print(upload_to_firebase_storage(r'C:\Users\nguye\Downloads\kipe_logo.jpg'))






