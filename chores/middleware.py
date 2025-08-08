from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that don't require authentication
        exempt_urls = [
            reverse('login'),
            '/admin/',  # Allow admin access
        ]
        
        # Check if the current path is exempt
        if any(request.path.startswith(url) for url in exempt_urls):
            response = self.get_response(request)
            return response
        
        # Check if user is logged in
        if not request.session.get('user_id'):
            return redirect('login')
        
        response = self.get_response(request)
        return response
