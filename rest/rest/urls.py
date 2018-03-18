from django.urls import include, path
from django.contrib.admin import site as admin_site

urlpatterns = [
    path('applications/', include('apps.applications.urls')),
    path('worksheets/', include('apps.worksheets.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin_site.urls),
]
