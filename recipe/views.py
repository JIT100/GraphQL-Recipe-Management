from django.shortcuts import redirect
from rest_framework_simplejwt.authentication import JWTAuthentication


def home_redirect(request):
    """Redirect to /graphql/ if authenticated, otherwise to the token obtain endpoint."""
    try:
        auth = JWTAuthentication()
        auth_result = auth.authenticate(request)
        if auth_result is not None:
            user, token = auth_result
            request.user = user
    except Exception:
        pass

    if getattr(request, 'user', None) and request.user.is_authenticated:
        return redirect('/graphql/')
    return redirect('/api/token/')