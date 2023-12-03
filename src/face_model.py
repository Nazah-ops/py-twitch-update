from keras.models import model_from_json
import cv2
import numpy as np
import face_recognition
from hide_print import HiddenPrints

class FaceModel:

    @staticmethod
    def read_video_emotion(video: str) -> dict:

        vidcap = cv2.VideoCapture(f'/app/files/clips/{video}')
        success,image = vidcap.read()
        
        if not success:
            raise Exception("Video not correctly loaded, presumably not there")
        
        results_percentage = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'neutral': 0, 'sad': 0, 'surprise': 0}
        labels = {0 : 'angry', 1 : 'disgust', 2 : 'fear', 3 : 'happy', 4 : 'neutral', 5 : 'sad', 6 : 'surprise'}

        
        
        def extract_features(face_image):
            smaller_face_image = cv2.resize(face_image,(48,48))
            feature = np.array(smaller_face_image)
            feature = feature.reshape(1,48,48,1)
            return feature/255.0
        
        json_file = open("/app/files/models/emotion/emotiondetector.json", "r")
        model = model_from_json(json_file.read())
        json_file.close()
        model.load_weights("/app/files/models/emotion/emotiondetector.h5")

        multp = 3
        skip = 0
        
        while success:
            success,image = vidcap.read()

            if success is False:
                break

            #Elaborate 1 in each X frames for efficency. Faces don't change that quicly
            if skip < 90:
                skip += 1
                continue

            skip = 0
            
            #Reduce the size of the image to examine for efficency purposes
            face_locations = face_recognition.face_locations(cv2.resize(image, (0, 0), fx=1/multp, fy=1/multp), model="cnn")
            
            if len(face_locations) == 0:
                continue
            
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            top, right, bottom, left = face_locations[0]
            face_image = gray[top*multp : bottom*multp, left*multp : right*multp]
            
            
            extracted_img = extract_features(face_image)
            with HiddenPrints():
                pred = model.predict(extracted_img)
            results_percentage[labels[pred.argmax()]] += 1

        return results_percentage