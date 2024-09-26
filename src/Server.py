from flask import Flask, request, jsonify
from flask_cors import CORS
import mediapipe as mp 
import base64
import json
from keras.models import load_model
from keras.models import model_from_json
import numpy as np
from Words_Function import*
from Letters_Function import*
from collections import deque


class User:
    def __init__(self, name, last_name, email, password, username, how):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.username = username
        self.how = how

    def as_dict(self):
        return {
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'how': self.how
        }

app = Flask(__name__)
CORS(app)
# Define a list of users to store the registered users
#users = [User('Naama', 'Lugasi', 'naamae2003@gmail.com', '214312837', 'naama1234', 'family')]

# with open('users.json', 'r') as f:
#     users = json.load(f)
users = []

@app.route('/signup', methods=['POST'])
def signup():
    # Get the user details from the request body
    user = request.get_json()
    users.append(user)
    # with open('users.json', 'w') as f:
    #     json.dump(users, f)
    # Return a success response
    return jsonify({'message': 'User was successfully signed up!'})

@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Get the user credentials from the request body
    user_credentials = request.data.decode('utf-8')
    # Check if the user exists in the list of users

    # Convert the JSON string to a Python dictionary
    login_dict = json.loads(user_credentials)
    # for user in users:
    #     if user.username == user_credentials['username'] and user.password == user_credentials['password']:
    #         # User was successfully authenticated
    
    # Check if the username and password match the values in the data dictionary
    if login_dict['username'] in users and login_dict['password'] == users[login_dict['username']]['password']:
            return jsonify({'message': 'User was successfully authenticated!'})
    # User could not be authenticated
    return jsonify({'message': 'Invalid username or password'})

# @app.route('/users', methods=['GET'])
# def get_users():
#     return jsonify(users)



threshold = 0.7

MAX_QUEUE_SIZE = 30
my_queue_w = []


def add_to_queue_w(item):
    global my_queue_w
    my_queue_w.append(item)
    if len(my_queue_w) > MAX_QUEUE_SIZE:
        my_queue_w.pop(0)
@app.route('/process_frames', methods=['POST'])
def process_frames():
  w_prediction = []
  labels = np.array(['hello', 'thanks','sorry','good morning','a','b','c'])
  
  w_model = load_model(r'models\sign4_lang_model.h5')
  w_model.load_weights(r'models\SLD_val_loss')
  data_url = request.json['dataURL']
  image_data = base64.b64decode(data_url.split(',')[1])
  img_bgr = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

#   with open('frame.png', 'wb') as f:
#     f.write(image_data)
#   return 'Frame received'
  with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            img, results = mediapipe_detection_w(img_bgr, holistic)
            holistic_drawing_w(img, results)
            keypoints = extract_keypoints_w(results)
            add_to_queue_w(keypoints)
            #sentence.append(keypoints)
            #if len(my_queue_w) == MAX_QUEUE_SIZE:
            res = w_model.predict(np.expand_dims(my_queue_w, axis=0))[0]
            w_prediction.append(np.argmax(res))
            if np.unique(w_prediction[-10:])[0]==np.argmax(res):
                    if res[np.argmax(res)] > threshold:
                      label = str(labels[np.argmax(res)])
                      print(label)
  return jsonify({'message': 'OK', 'label': label}) 
  #return jsonify({'message': 'OK', 'label':  'unknown'}) 



# לאותיות
my_queue = []

def add_to_queue(item):
    global my_queue
    my_queue.append(item)
    if len(my_queue) > MAX_QUEUE_SIZE:
        my_queue.pop(0)
@app.route('/process_frame', methods=['POST'])
def process_frame():
  actions = np.array(['A','B','C'])
  json_file = open(r"models\model.json", "r")
  model_json = json_file.read()
  json_file.close()
  l_model = model_from_json(model_json)
  l_model.load_weights(r"models\model.h5")
  l_predictions = []
  l_data_url = request.json['dataURL']
  l_image_data = base64.b64decode(l_data_url.split(',')[1])
  with open('frame.png', 'wb') as f:
    f.write(l_image_data)
  l_img_bgr = cv2.imdecode(np.frombuffer(l_image_data, np.uint8), cv2.IMREAD_COLOR)
  
#   return 'Frame received'

  with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
        # Make detections
        cropframe=l_img_bgr[40:400,0:300]
        # print(frame.shape)
        l_img_bgr=cv2.rectangle(l_img_bgr,(0,40),(300,400),255,2)
        l_image, l_results = mediapipe_detection(cropframe, hands)
        # print(results)
        
        # Draw landmarks
        draw_styled_landmarks(l_image, l_results)
        # 2. Prediction logic
        l_keypoints = extract_keypoints(l_results)
        #l_sequence.append(l_keypoints)
        #l_sequence = l_sequence[-30:]
        add_to_queue(l_keypoints)
        #if len(l_sequence) == l_sequence.maxlen:
            #oldest_frame = l_sequence.popleft()


        try: 
            #if len(l_sequence) == 30:
            l_res = l_model.predict(np.expand_dims(my_queue, axis=0))[0]
            l_predictions.append(np.argmax(l_res))             
                
            #3. Viz logic
            if np.unique(l_predictions[-10:])[0]==np.argmax(l_res): 
                if l_res[np.argmax(l_res)] > threshold: 
                        l_answer=str(actions[np.argmax(l_res)])
        except Exception as e:
            pass
  return jsonify({'message': 'OK', 'label': l_answer})



if __name__ == '__main__':
    app.run()