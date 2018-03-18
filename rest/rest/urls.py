from django.urls import include, path

urlpatterns = [
    path('credits/', include('apps.credits.urls')),
    path('partners/', include('apps.partners.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
