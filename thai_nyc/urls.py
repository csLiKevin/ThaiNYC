from django.conf.urls import url
from django.contrib import admin

from restaurants.views import Home

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^$", Home.as_view(), name="home")
]
