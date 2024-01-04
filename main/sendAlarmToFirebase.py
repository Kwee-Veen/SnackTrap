import firebase_admin, datetime, json, os
from firebase_admin import credentials, firestore, storage, db

# Configuring Firebase settings and variables
cred=credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'snacktrap-9661f.appspot.com',
    'databaseURL': 'https://snacktrap-9661f-default-rtdb.europe-west1.firebasedatabase.app/'
})
bucket = storage.bucket()
ref = db.reference('/')
home_ref = ref.child('file')


# Function that creates a temporary json-format file whenever an alarm is triggered, including the alarm status and the date and time it was triggered.
# The json file is pushed to Firebase via the storeFileFB functions, before being deleted (locally only, still available on Firebase)
def alarm_event():
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    time = datetime.datetime.now().strftime("%H_%M_%S")
    file = open(f"alarm_{time}.json", 'w')
    event = (f'{{"Alarm": "1", "Time": "{now}"}}')
    event_json = json.loads(event)
    json.dump(event_json, file)
    file.close()
    fileLoc = f'/home/carbot/alarm_{time}.json'
    store_file(fileLoc)
    push_db(fileLoc, now)
    print(f'Alarm event {event} pushed to Firebase')
    os.remove(f'/home/carbot/alarm_{time}.json')

# Function pushes the alarm file to Firebase's Storage
def store_file(fileLoc):
    filename=os.path.basename(fileLoc)
    blob = bucket.blob(filename)
    outfile=fileLoc
    blob.upload_from_filename(outfile)

# Function pushes the alarm event file reference to Firebase's Realtime DB
def push_db(fileLoc, time):
  filename=os.path.basename(fileLoc)
  home_ref.push({
      'filename': filename,
      'timestamp': time}
  )
