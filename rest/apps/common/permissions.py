import logging
from django.http import Http404
from rest_framework import permissions

log = logging.getLogger('apps.common')
SAFE_METHODS = ('HEAD', 'OPTIONS')


class DjangoModelPermissionsWithRead(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.read_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class IsOwnerOrDjangoModelPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.read_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == getattr(obj, 'owner', None)
