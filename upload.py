import urllib, json
import requests

from picamera import PiCamera
from time import sleep
from pygame import mixer
import RPi.GPIO as GPIO


camera = PiCamera()

GPIO.setmode(GPIO.BCM)
allPins=[12,18,23,24,25]

for pin in allPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)


currentEmotions = []


while True:
    try:
        sleep(1)
        currentEmotions = []
        
        camera.resolution = (1216, 912)
        #camera.resolution = (640, 480)
        camera.start_preview()
        sleep(1)
        camera.capture('/home/pi/Desktop/image.jpg')
        camera.stop_preview()
        img_filename = '/home/pi/Desktop/image.jpg'
        with open(img_filename, 'rb') as f:
            img_data = f.read()

        # Replace the subscription_key string value with your valid subscription key.
        subscription_key = 'c347f84bbcec4b53914e4ad97b584d31'
    
        

        ## Request headers.
        header = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key,
        }

        # Request parameters.
        params = urllib.parse.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        })
        
        

        api_url = "https://eastus.api.cognitive.microsoft.com/face/v1.0/detect?%s"%params

        r = requests.post(api_url,
        #                  params=params,
                          headers=header,
                          data=img_data)

        faces = json.loads(r.text)
         
        print("detected ", len(faces) )
        
        
 
        
        
        if len(faces) == 0:
            for pin in allPins:
                GPIO.output(pin, False)
            
          
        
        for user in faces:
            emotions = ['anger','contempt','disgust','fear','happiness','neutral','sadness','surprise']
            emotionvalues=[];
            emotionvalues.append(float(user["faceAttributes"]["emotion"]["anger"]))  #red
            emotionvalues.append(float(user["faceAttributes"]["emotion"]["contempt"])) #red
            emotionvalues.append(float(user["faceAttributes"]["emotion"]["disgust"]))#red
            
            emotionvalues.append(float(user["faceAttributes"]["emotion"]["fear"])) #blue            
            emotionvalues.append(float(user["faceAttributes"]["emotion"]["happiness"])) #white            
            emotionvalues.append(float(user["faceAttributes"]["emotion"]["neutral"])) # green            
            emotionvalues.append(float(user["faceAttributes"]["emotion"]["sadness"])) #yellow            
            emotionvalues.append(float(user["faceAttributes"]["emotion"]["surprise"])) #blue
            maxEmotion = max(emotionvalues)
            indexOfVal = emotionvalues.index(maxEmotion)
            emotion = emotions[indexOfVal]
            #white 12
            #red 18
            #green 24
            #blue 23
            #yellow 25
            
             
            
            if emotion == "happiness":
                currentEmotions.append (12)
            if emotion == "anger" or emotion == "contempt" or emotion == "disgust":
                currentEmotions.append (18)
            if emotion == "fear" or emotion == "surprise":
                currentEmotions.append (23)
            if emotion == "sadness":
                currentEmotions.append (25)
            if emotion == "neutral":
                currentEmotions.append (24)

             
            print(emotion)
            
        
        for pin in allPins:
            if pin in currentEmotions:
                GPIO.output(pin, True)
            else:
                GPIO.output(pin, False)
            


            
    
            #print(user["faceAttributes"]["emotion"])
    except:
        print("Error")
    
 
