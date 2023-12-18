from django.shortcuts import redirect
from django.urls import reverse


class AdminRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not request.user.is_superuser:
            return redirect(reverse('main'))

        response = self.get_response(request)
        return response
