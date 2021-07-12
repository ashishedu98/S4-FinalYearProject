import math
from sklearn import neighbors
import datetime
import time
import os
import os.path
import face_recognition
import pickle
import cv2
import numpy as np
from PIL import Image, ImageDraw
from face_recognition.face_recognition_cli import image_files_in_folder
import shutil
import psycopg2
import json
import requests
import urllib.request
moveimg = 'D:\\ASHSIH\\ENGG\\VIII SEM\\project\\Detected_images\\'
count = 0
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
camera_location = 'BMSCE'




def predict(X_img, knn_clf=None, model_path=None, distance_threshold=0.4):
    """
    Recognizes faces in given image using a trained KNN classifier
    :param X_img_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
    :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
           of mis-classifying an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'unknown' will be returned.
    """
    # if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
    #raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception(
            "Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    #X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(
        X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <=
                   distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


def show_prediction_labels_on_image(frame, predictions):
    """
    Shows the face recognition results visually.
    :param img_path: path to image to be recognized
    :param predictions: results of the predict function
    :return:
    """
    # img_path=os.path.join(src,img_name)
    #pil_image = Image.open(img_path).convert("RGB")
    #draw = ImageDraw.Draw(X_img)
    # save_path=os.path.join("result",img_name)
    final_name = ''
    for name, (top, right, bottom, left) in predictions:
        # Draw a box around the face using the Pillow module
        #draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # There's a bug in Pillow where it blows up with non-UTF-8 text
        # when using the default bitmap font
        #name = name.encode("UTF-8")

        # Draw a label with a name below the face
        #text_width, text_height = draw.textsize(name)
        #draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        #draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
        cv2.rectangle(frame, (left, bottom - 35),
                      (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 1.0, (255, 255, 255), 1)
        if final_name == '':
            final_name = name
        else:
            final_name = final_name+'_'+name

    ts = time.time()
    final_name = final_name+"_" + \
        datetime.datetime.fromtimestamp(
            ts).strftime('%Y_%m_%d_%H_%M_%S')+".jpg"
    save_path = 'result/'+str(final_name)
    cv2.imwrite(save_path, frame)

    # Remove the drawing library from memory as per the Pillow docs
    #del draw

    # Display the resulting image
    # pil_image.show()


# if __name__ == "__main__":
#     # STEP 1: Train the KNN classifier and save it to disk
#     # Once the model is trained and saved, you can skip this step next time.
#     #print("Training KNN classifier...")
#     #classifier = train("training_pics", model_save_path="trained_model.clf", n_neighbors=5)
#     #print("Training complete!")

#     # STEP 2: Using the trained classifier, make predictions for unknown images
#     # for image_file in os.listdir("test"):
#     #full_file_path = os.path.join("test", image_file)

#     cam = cv2.VideoCapture("https://drive.google.com/uc?id=1xYoIWgSDrelz5lFDe1F-kOw_sqAYH2kD")  # thread1 start
#     flag = True
#     #print("Looking for faces in {}".format(image_file))
#     while flag:
#         # Find all people in the image using a trained classifier model
#         # Note: You can pass in either a classifier file name or a classifier model instance
#         #global count
#         # time.sleep(3)
#         count += 1
#         # moveit=moveimg+'d'+str(count)+'.jpg'
#         cur_time = datetime.datetime.now()
#         print(cur_time)
#         # image_name='d'+str(count)+'.jpg'

#         image_name = str(cur_time)
#         img = image_name.split(" ")
#         img2 = image_name.replace(' ', '-')
#         img2 = img2.replace(':', '-')
#         img1 = img[1].split(".")
#         img1[0] = img1[0].replace(':', '-')
#         image_name = img[0]+'-'+img1[0]+'.jpg'
#         image_name1 = img[0]+'-'+img1[0]
#         print(image_name)

#         ret, frame = cam.read()
#         X_img = frame[:, :, ::-1]
#         #rgb_small_frame = small_frame[:, :, ::-1]
#         #image = face_recognition.load_image_file(X_img)
#         # X_img=cv2.imread(something)
#         face_bounding_boxes = face_recognition.face_locations(
#             X_img)  # thread2 start

#         if len(face_bounding_boxes) != 0:  # thread1 end
#             #cv2.imwrite(os.path.join(moveimg , image_name), X_img)
#             # shutil.move(image,moveimg)

#             predictions = predict(X_img, model_path="C:\\Users\\Narashima\\Downloads\\p1\\security\\secapp\\trained_model.clf")
#             if len(predictions) != 0:
#                 show_prediction_labels_on_image(frame, predictions)
#                 image_path = str(moveimg)+str(image_name)
#                 conn = psycopg2.connect(
#                     database="criminal_records", user="postgres", password="password")
#                 cur = conn.cursor()
#                 current_time = datetime.datetime.now()
#                 all_suspects = ' '
#                 for suspect in predictions:
#                     cv2.imwrite(os.path.join(moveimg, image_name), frame)

#                     headers = {"Authorization": "Bearer ya29.a0AfH6SMAzBZIVymZc4tPQk4CRINRBSS_-ZTlo8uf-b17EEBVl99uuksD-1t45Zxo7xKB_VbaUGH0R6CqQGz5FApSAH0juu_AFYfH2RuHjCWQGK1aIrAPtP9G6UIILGzlE5fhttnGQNgDE9ojkZwBn0-vQ7O-Nuw"}
#                     para = {
#                         "name": "sample.jpg",
#                         "parents": ["1jiaXWL9EnlgOfkDj0F9TKK7Owq3RcMbE"]
#                     }
#                     files = {
#                         'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
#                         'file': open(image_path, "rb")
#                     }
#                     r = requests.post(
#                         "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
#                         headers=headers,
#                         files=files
#                     )
#                     var = json.loads(r.text)
#                     print(r.text)
#                     print(var)
#                     baseurl = "https://drive.google.com/uc?id="
#                     imglink = baseurl+str(var['id'])
#                     print(imglink)
#                     if suspect[0] == "unknown":
#                         suspect_id = int(999)
#                         url = urllib.request.urlopen("http://127.0.0.1:8000/getSuspectinfo/?sid="+str(suspect_id))
#                         #data = json.load(url)
#                         #print(data)
#                         cur.execute("UPDATE secapp_suspect_profiles set last_pic=%s where sid=%s;", (imglink, suspect_id))
#                         conn.commit()
                        
#                     else:
#                         suspect_id = int(suspect[0][:3])
#                         #cur.execute("INSERT INTO recognised(SID,RECOGNISED_TIME,RECOGNISED_LOCATION,RECOGNISED_PIC) VALUES (%s, %s, %s, %s);" ,(suspect_id,current_time,camera_location,image_path))
#                         # conn.commit()
#                         cur.execute("UPDATE secapp_suspect_profiles set location=%s,last_found=%s,last_pic=%s where sid=%s;", (
#                             camera_location, current_time, imglink, suspect_id))
#                         conn.commit()
#                         print("inserted and updated successfully")
#                         all_suspects = all_suspects+','+str(suspect_id)
#                         url = urllib.request.urlopen(
#                             "http://127.0.0.1:8000/getSuspectinfo/?sid="+str(suspect_id))
#                         #data = json.load(url)
#                         #print(data)
#                         if(all_suspects != ''):
#                             cur.execute("INSERT INTO secapp_suspect_recognised(sid,detect_time,detect_location,detect_pic) VALUES (%s, %s, %s, %s);", (
#                                 all_suspects, current_time, camera_location, imglink))
#                             conn.commit()

#                 conn.close()  # thread2 close

#         cv2.imshow('Video', frame)

#         # Hit 'q' on the keyboard to quit!
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         flag = False

# # Release handle to the webcam
# cam.release()
# cv2.destroyAllWindows()
