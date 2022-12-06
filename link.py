import requests
import base64

f = open('snapshot.jpg', 'rb')

#with open("snapshot.jpg", "rb") as img_file:
#    b64_string = base64.b64encode(img_file.read())

#response = requests.post('http://13.124.202.212:3000/polaroid/uploaddiaryimage',data={"image":b64_string, "email":"mimo", "petname":"토토"})
response = requests.post('http://13.124.202.212:3000/polaroid/uploaddiaryimage', files={'files':f}, data={'email':'mimo','petname':'토토'})

print(response)
