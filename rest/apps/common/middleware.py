from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from .models import Organization


def get_checking_uri_list():
    return [choice[0] for choice in Organization.API_URL_CHOICES]


class CheckAPIAccess:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not any(request.path.startswith(uri)
                   for uri in get_checking_uri_list()):
            return self.get_response(request)
        user: User = request.user
        organization = getattr(user, 'organization', None)
        if user.is_authenticated and organization:
            allowed_uri = organization.api_access
            if request.path.startswith(allowed_uri):
                return self.get_response(request)
            elif allowed_uri:
                return redirect(allowed_uri)
        elif user.is_superuser:
            return self.get_response(request)
        return redirect('no-access')
