from rest_framework import views
from rest_framework.response import Response
from django.shortcuts import redirect


class NoAccessView(views.APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        organization = getattr(user, 'organization', None)
        if organization and organization.api_access:
            return redirect(organization.api_access)
        resp = Response({
            'details': 'You have no access to any API.'
        })
        resp.status_code = 403
        return resp
