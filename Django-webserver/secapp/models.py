# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from secapp.signals import image_signal
import datetime
#from .KNN import *
#from .FRv5 import recognition

current_time = str(datetime.datetime.now())
current_time = current_time[:len(current_time)-7]



class Suspect_recognised(models.Model):     #Recognition table
    sid = models.CharField(max_length=100)
    detect_time = models.CharField(max_length=100,help_text="Format: YYYY-MM-DD HH:MM:SS",default=current_time)
    detect_location = models.CharField(max_length = 100)
    detect_pic = models.CharField(max_length=100)

    def __str__(self):
        return str(self.sid)


class Suspect_profiles(models.Model):     #primary records
    sid = models.IntegerField(blank=True,null = True)
    name = models.CharField(max_length = 100)
    age = models.IntegerField(max_length = 100)
    location = models.CharField(max_length = 100)
    threat = models.IntegerField(blank = True,null = True)
    last_found = models.CharField(max_length=100,help_text="Format: YYYY-MM-DD HH:MM:SS",default=current_time)
    image = models.CharField(max_length=100)
    last_pic = models.CharField(max_length=100)
    cases = models.CharField(max_length=100,null=True)
    date_of_birth = models.CharField(max_length=100,help_text="Format:YYYY-MM-DD",null=True)

    def __str__(self):
        return self.name

# class Face_detects(models.Model):      #Detection table
#     face_img = models.CharField(max_length=100)

# @receiver(pre_save,sender=Suspect_names)
# def add_image_to_detects(sender,instance,**kwargs):
#     id_given = instance.sid
#     detected_time = instance.last_found
#     detected_location = instance.location
#     img = instance.last_pic
#     sd = Suspect_detects(sid=id_given,detect_time=detected_time,detect_location=detected_location,detect_pic=img)
#     sd.save()

# @receiver(post_save,sender=Suspect_names)
# def notify(sender,**kwargs):
#     confirm()
# def confirm():
#     print("Added record to both tables")


# @receiver(post_save,sender=Face_detects)
# def receiveFaceToDetect(sender,instance,**kwargs):
#     """face = instance.face_img
#     ret,frame=cam.read()
#     X_img=frame [:, :, ::-1]
#     predictions = predict(X_img, model_path="trained_model.clf")

#     if len(predictions)!=0:
#         image_path = show_prediction_labels_on_image(frame, predictions)
#         for name, (top, right, bottom, left) in predictions:
#             now = datetime.now()        
#             current_time = now.strftime("%H:%M:%S")
#             current_time = str(current_time)
#             location = "Banashankari 3rd Stage"
#             sn = Suspect_names.objects.filter(name=suspect_name).update(last_pic=image_path,last_found=current_time)   #add into primary records
#             detected_id = sn.id
#             sd = Suspect_detects(sid=detected_id,detect_pic=image_path,detect_time=current_time,detect_location=location) #add into recognition table
#             sd.save()
#             print("image received and updated!!!!!!!!!")"""




# Create your models here.
