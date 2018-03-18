from django.urls import path
from django.contrib.admin import site as admin_site

urlpatterns = [
    path('', admin_site.urls),
]
