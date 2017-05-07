# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from restaurants.models import Restaurant, Grade, Inspection


admin.site.register(Restaurant)
admin.site.register(Inspection)
admin.site.register(Grade)
