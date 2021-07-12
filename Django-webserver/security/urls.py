"""security URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from os import name
from django.conf.urls import url
from django.contrib import admin
from secapp.views import *
from django.http import HttpResponse
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('hostpage',hostpage,name='hostpage'),
    url('showRecentRecognition',showRecentRecognition,name='showRecentRecognition'),
    url('liveRecognition',liveRecognition,name='liveRecognition'),
    url('getSuspectinfo',getSuspectinfo,name="getSuspectinfo"),
    #url('update2',update_confirm,name="update_function"),
    #url('receiveImage',receiveImage),
   #url('receiveFace',receiveFace),
    #url('update1',u1),
    #url('updated/',add,name="my_function"),
    #url('about',contact),
    url('all_suspects',all_suspects,name='all_suspects'),
    url('all_recognitions',all_recognitions,name='all_recognitions'),
    #url('',home),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)