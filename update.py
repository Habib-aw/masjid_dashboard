import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import json
import os
import sys

imageDir = "images/downloadedImages/"
uid = sys.argv[1]
code = sys.argv[2]
projectName = sys.argv[3]
email = "firebase-adminsdk-"+code+"@"+projectName+".iam.gserviceaccount.com"
private_key = "-----BEGIN PRIVATE KEY-----\n"+sys.argv[4].replace("#"," ")+"\n-----END PRIVATE KEY-----\n"
cred = credentials.Certificate({
  "type": "service_account",
  "private_key": private_key.replace("#","\n"),
  "client_email": email,
  "token_uri": "https://oauth2.googleapis.com/token"
}
)

firebase_admin.initialize_app(cred,{
    "databaseURL":"https://"+projectName+"-default-rtdb.firebaseio.com",
    "storageBucket": projectName+".appspot.com"
})
jsonData = db.reference("users/"+uid).get()
data = jsonData["frequent"]["receiver"]
times = jsonData['infrequent']
with open('times.json', 'w', encoding='utf-8') as f:
    json.dump(times, f, ensure_ascii=False, indent=4)
with open('db.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
imageSlides = data['slides']['imageSlide']
bucket = storage.bucket()
downloadedImages = os.listdir(imageDir)
for i in range(len(imageSlides)):
    if imageSlides[i]['imageName'] in downloadedImages:
        continue
    imgName = imageSlides[i]['imageName']
    blob = bucket.blob(uid+'/'+imgName)
    blob.download_to_filename(imageDir+imgName)