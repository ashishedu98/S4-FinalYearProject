# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Suspect_profiles,Suspect_recognised

admin.site.register(Suspect_profiles)
admin.site.register(Suspect_recognised)

# Register your models here.
