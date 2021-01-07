import firebase_admin #imports firebase_admin package
from firebase_admin import credentials, firestore, storage, db #imports credentials, firestore, storage and db sections of firebase_admin package
import os #imports os package

cred=credentials.Certificate('./serviceAccountKey.json') #creates cred value which is defined as credentials pulled from the serviceAccountKey.json file
firebase_admin.initialize_app(cred, {
    'storageBucket': 'dogbarkalertdatabase.appspot.com',
    'databaseURL': 'https://dogbarkalertdatabase-default-rtdb.firebaseio.com/'
}) #initialises firebase using credentials above and setting the storageBucket and databaseURL as the values taken from the firebase account

bucket = storage.bucket() #default bucket values as per firebase storage API set up

ref = db.reference('/')
home_ref = ref.child('file')

def store_file(fileLoc): #creates store_file method which takes the images captured from camera and stores them in the Storage Section of Firebase

    filename=os.path.basename(fileLoc)

    # Store File in FB Bucket
    blob = bucket.blob(filename)
    outfile=fileLoc
    blob.upload_from_filename(outfile)

def push_db(fileLoc, time): #creates push_db method which takes the image captured and timestamp and pushes them to the firebase realtime database

    filename=os.path.basename(fileLoc)

    home_ref.push({
	'image': filename,
	'timestamp': time}
    )
