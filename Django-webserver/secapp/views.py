# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.http import response
from django.http.response import JsonResponse

from django.shortcuts import render
from django.http import HttpResponse
from secapp.models import *
from datetime import datetime
from django.dispatch import Signal,receiver
from .signals import image_signal
from .KNN import *
from rest_framework.decorators import api_view
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests
import json


trained_model_path="D:\\ASHSIH\\ENGG\\VIII SEM\\project\\"


def all_suspects(request):  #displays all suspects in the table
    s = Suspect_profiles.objects.all()
    responseData = []
    for suspect in s:
        item = {
            "sid":suspect.sid,
            "names":suspect.name,
            "detect_location":suspect.location,
            "threats":suspect.threat,
            "detect_time":suspect.last_found,
            "image":suspect.image,  
            
        }
        responseData.append(item)

    return JsonResponse(responseData,safe=False)

def all_recognitions(request):  #displays all suspects in the table
    s = Suspect_recognised.objects.all()
    responseData = []
    for suspect in s:
        sids = suspect.sid.split(",")[1:]
        # print(sids)
        names = ""
        threats = ""
        for i in sids:
            id = int(i)
            name = Suspect_profiles.objects.filter(sid=id)[0].name
            names+=","+str(name)
            threat = Suspect_profiles.objects.filter(sid=id)[0].threat
            threats+=","+str(threat)

        # print(names)
        # print(threats)
        names = names[1:]
        threats = threats[1:]

        item = {
            "sid":suspect.sid[2:],
            "names":names,
            "threats":threats,
            "detect_time":suspect.detect_time,
            "detect_location":suspect.detect_location,
            "detect_pic":suspect.detect_pic
        }
        responseData.append(item)

    return JsonResponse(responseData,safe=False)

        
 

# def home(request):
#     return render(request,"home.html")

# def contact(request):  #return webpage to add another suspect to the existing table
#     return render(request,"entry.html")

# def add(request):                    #this one adds a new record into the table by taking values from entry.html and displays in added.html
#     sid = request.GET.get("sid")
#     sid = int(sid)
#     name = request.GET.get("name")
#     age = request.GET.get("age")
#     age = int(age)
#     location = request.GET.get("location")
#     threat = request.GET.get("threat")
#     threat = int(threat)
#     lst = request.GET.get("lst")
#     #image = request.GET.get("image")
#     a = Suspect_profiles.objects.all()

#     for s in a:
#         if s.sid == sid:
#             return render(request,"same_id_error.html")   #in case same id is inserted, this error page is shown
#     s = Suspect_profiles(sid=sid,name=name,age=age,location=location,threat=threat,last_found=lst)
#     #s.image.name=u'suspect_images\1.jpg'
#     #s.image.path=u'C:\\Users\\Narashima\\Desktop\\suspects\\1.jpg'
#     image = u"C:\\Users\\Narashima\\Desktop\\suspects\\3.jpg"
#     #s.image = u'https://drive.google.com/file/d/1rDSZ7jAQlH-2nK_njN3wxRqTTsmzGK_U/view?usp=sharing'
#     s.image = image
  
#     s.save()
#     sd = Suspect_recognised(sid=sid,detect_time=lst,detect_location=location)
#     sd.image=image
#     sd.save()

#     return render(request,"added.html",{'sid':sid,'name':name,"age":age,"location":location,"threat":threat,"lst":lst,"s":s})

# def u1(request):
#     return render(request,"update1.html")

# def update_confirm(request):     #this one updates the values of the records.it takes the parameters from update1.html and displays them in update2.html
#     sid = request.GET.get("sid")
#     field = request.GET.get("field")
#     value = request.GET.get("value")
#     sid = int(sid)
#     suspect = Suspect_profiles.objects.filter(sid=sid) #suspect is an array of all objects returned based on the condition.Here, it is an aarray with one element(since id is unique)
#     if field == "name":
#         suspect.update(name=value)
#     elif field == "age":    
#         value = int(value)    #convert into interger;age is int
#         suspect.update(age=value)
#     elif field == "location":
#         suspect.update(location=value)
#         now = datetime.now()           #not only location, but also update the time
#         current_time = now.strftime("%H:%M:%S")
#         current_time = str(current_time)
#         suspect.update(last_found=current_time)
#         sd = Suspect_recognised(sid=sid,detect_time=current_time,detect_location=value)
#         sd.save()
#     elif field == "threat":
#         value = int(value)    #convert into interger because threat is an interger
#         suspect.update(threat=value)
#     elif field == "lst":
#         suspect.update(last_found=value)
#         loc = suspect[0].location    #because its an array with only one element
#         sd = Suspect_recognised(sid=sid,detect_time=value,detect_location=loc)
#         sd.save()
#     return render(request,"update2.html",{'sid':sid,'field':field,'value':value})

# def receiveImage(request):
#     sid = request.GET.get("sid")
#     image = request.GET.get("image")
#     now = datetime.now()           #not only location, but also update the time
#     current_time = now.strftime("%H:%M:%S")
#     current_time = str(current_time)
#     suspect = Suspect_profiles.objects.filter(sid=sid)
#     suspect.update(last_pic=image,last_found=current_time)
#     sd = Suspect_recognised.objects.filter(sid=sid)
#     sd.update(detect_time=current_time,detect_pic=image)
#     print("Its done!!!!!!!!!!!!")
#     return render(request,"imagerecieved.html")

# # def receiveFace(request):
# #     image = request.GET.get("image")
# #     f.save()
# #     #image_signal.send(sender=Face_detects,newface=image,hasreceived=True)
# #     print("Added unknown image!!!!")

#     return render(request,"facereceived.html")

def getSuspectinfo(request):
    
    sid = request.GET.get("sid")
    print(sid)
    sid = int(sid)
    suspects = Suspect_profiles.objects.filter(sid=sid)
    if len(suspects) == 0:
        return render(request,"no_id_error.html")
    suspect = suspects[0]
    name=suspect.name
    age=suspect.age
    location = suspect.location
    threat = suspect.threat
    last_found = suspect.last_found
    image = suspect.image
    lastpic = suspect.last_pic
    responseData = {
        "sid":sid,
        "name":name,
        "age":age,
        "location":location,
        "threat":threat,
        "lst":last_found,
        "image":image,
        "lastpic":lastpic,
        "date_of_birth":suspect.date_of_birth,
        "cases":suspect.cases}
    #return render(request,"recent_detect.html",{"lastpic":lastpic})
    return JsonResponse(responseData)

@api_view(['POST'])
def liveRecognition(request):
    camera_location = request.data['location']
    image = request.data['image']
    #https://firebasestorage.googleapis.com/v0/b/s3-frontend.appspot.com/o/images%2Fcriminaltest.jpg?alt=media&token=e031a73d-2cb9-4778-bd70-d4506303340a
    cam = cv2.VideoCapture(image)  # thread1 start
    flag = True
    suspect_id = int(999)
    #print("Looking for faces in {}".format(image_file))
    while flag:
        # Find all people in the image using a trained classifier model
        # Note: You can pass in either a classifier file name or a classifier model instance
        #global count
        # time.sleep(3)
        #count += 1
        # moveit=moveimg+'d'+str(count)+'.jpg'
        cur_time = datetime.datetime.now()
        print(cur_time)
        # image_name='d'+str(count)+'.jpg'

        image_name = str(cur_time)
        img = image_name.split(" ")
        img2 = image_name.replace(' ', '-')
        img2 = img2.replace(':', '-')
        img1 = img[1].split(".")
        img1[0] = img1[0].replace(':', '-')
        image_name = img[0]+'-'+img1[0]+'.jpg'
        image_name1 = img[0]+'-'+img1[0]
        print(image_name)

        ret, frame = cam.read()
        X_img = frame[:, :, ::-1]
        #rgb_small_frame = small_frame[:, :, ::-1]
        #image = face_recognition.load_image_file(X_img)
        # X_img=cv2.imread(something)
        face_bounding_boxes = face_recognition.face_locations(X_img)  # thread2 start

        if len(face_bounding_boxes) != 0:  # thread1 end
            #cv2.imwrite(os.path.join(moveimg , image_name), X_img)
            # shutil.move(image,moveimg)

            predictions = predict(X_img, model_path=trained_model_path+"trained_model.clf")
            if len(predictions) != 0:
                show_prediction_labels_on_image(frame, predictions)
                image_path = str(moveimg)+str(image_name)
                conn = psycopg2.connect(
                    database="criminal_records", user="postgres", password="password",host=settings.HOST_NAME,port=settings.PORT_NUMBER)
                cur = conn.cursor()
                current_time = str(datetime.datetime.now())
                current_time = current_time[:len(current_time)-7]
                all_suspects = ' '
                for suspect in predictions:
                    cv2.imwrite(os.path.join(moveimg, image_name), frame)

                    headers = {"Authorization": "Bearer "+settings.TOKEN}
                    para = {
                        "name": "sample.jpg",
                        "parents": [settings.PARENT]
                    }
                    files = {   
                        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
                        'file': open(image_path, "rb")
                    }
                    r = requests.post(
                        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                        headers=headers,
                        files=files
                    )
                    var = json.loads(r.text)
                    print(r.text)
                    print(var)
                    baseurl = settings.BASE_URL
                    imglink = baseurl+str(var['id'])
                    print(imglink)
                    if suspect[0] == "unknown":
                        suspect_id = int(999)
                        
                        #data = json.load(url)
                        #print(data)
                        cur.execute("UPDATE secapp_suspect_profiles set last_pic=%s,last_found=%s where sid=%s;", (imglink, current_time, suspect_id))
                        conn.commit()
                        
                    else:
                        suspect_id = int(suspect[0][:3])
                        #cur.execute("INSERT INTO recognised(SID,RECOGNISED_TIME,RECOGNISED_LOCATION,RECOGNISED_PIC) VALUES (%s, %s, %s, %s);" ,(suspect_id,current_time,camera_location,image_path))
                        # conn.commit()
                        cur.execute("UPDATE secapp_suspect_profiles set location=%s,last_found=%s,last_pic=%s where sid=%s;", (
                            camera_location, current_time, imglink, suspect_id))
                        conn.commit()
                        print("inserted and updated successfully")
                        
                        all_suspects = all_suspects+','+str(suspect_id)
                        #data = json.load(url)
                        #print(data)
                        if(all_suspects != ''):
                            cur.execute("INSERT INTO secapp_suspect_recognised(sid,detect_time,detect_location,detect_pic) VALUES (%s, %s, %s, %s);", (
                                all_suspects, current_time, camera_location, imglink))
                            conn.commit()

                conn.close()  # thread2 close

        #cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        flag = False

    #all_suspects for all the suspects
    sid = int(suspect_id)
    suspects = Suspect_profiles.objects.filter(sid=sid)
    if len(suspects) == 0:
        return render(request,"no_id_error.html")
    suspect = suspects[0]
    name=suspect.name
    age=suspect.age
    location = suspect.location
    threat = suspect.threat
    last_found = suspect.last_found
    image = suspect.image
    lastpic = suspect.last_pic
    responseData = {"details":{"sid":sid,"name":name,"age":age,"location":location,"threat":threat,"last":last_found,
    "image":image,"date_of_birth":suspect.date_of_birth,
    "cases":suspect.cases},"lastpic":lastpic}
    #return render(request,"recent_detect.html",{"lastpic":lastpic})
    return JsonResponse(responseData)


def showRecentRecognition(request):
    rownumber = request.GET.get("rownumber")
    s = Suspect_recognised.objects.filter(id=rownumber)
    print(s)
    suspects = s[0]     #there may be multiple suspects in one image
    recentPic = suspects.detect_pic
    settings.MOST_RECENT_PIC = recentPic
    render(request,"home.html",{"image":settings.MOST_RECENT_PIC})
    ids = suspects.sid.split(",")[1:]    #ids will have a null string at the start
    print(ids)
    maxthreat = False
    update_data = {}
    data = []
    for id in ids:
        sid = int(id)
        suspect = Suspect_profiles.objects.filter(sid=sid)
        suspect = suspect[0]
        if suspect.threat == 5:
            maxthreat = True
            #Trigger a notification

        

        info = {
            "sid":str(sid),
            "name":suspect.name,
            "location":suspect.location,
            "threat":suspect.threat,
            "last_found":suspect.last_found,
            "profile_pic":suspect.image,
            "date_of_birth":suspect.date_of_birth,
            "cases":suspect.cases
        }
        data.append(info)
    update_data["details"] = data
    update_data["threat"] = maxthreat
    update_data["lastpic"] = suspect.last_pic

    

    settings.DATA = update_data
    #urllib.request.urlopen("http://4c0791b7f7cb.ngrok.io/lol?newData=Django")
    requests.post(settings.NODE_SERVER+'/lol',json.dumps(update_data),headers={"content-type":"application/json"})
    
    return JsonResponse(update_data,safe=False)
    #return render(request,"recentrecognition.html",{"rownumber":rownumber,"recentPic":recentPic})

def hostpage(request):
    return JsonResponse(settings.DATA,safe=False)
    #return render(request,"hostpage.html",{"mostRecentPic":settings.MOST_RECENT_PIC})
