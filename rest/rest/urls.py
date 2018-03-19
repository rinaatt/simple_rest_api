from django.urls import include, path
from apps.credits.urls import credits_router
from apps.partners.urls import partners_router
from apps.common.views import NoAccessView

urlpatterns = [
    path('partners/', include(partners_router.urls)),
    path('credits/', include(credits_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('no-access/', NoAccessView.as_view(), name='no-access')
]
