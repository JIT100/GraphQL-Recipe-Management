from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden

from rest_framework_simplejwt.authentication import JWTAuthentication

from . import schema as recipe_schema
from strawberry.django.views import GraphQLView


def auth_graphql_view(request):
    try:
        user_auth = JWTAuthentication()
        auth_result = user_auth.authenticate(request)
        if auth_result is not None:
            user, validated_token = auth_result
            request.user = user
    except Exception:
        pass

    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return HttpResponseForbidden("<h1> Authentication required. Kindly Login via the /api/token/ endpoint.</h1>")

    view = GraphQLView.as_view(schema=recipe_schema.schema)
    return view(request)


urlpatterns = [
    path('graphql/', csrf_exempt(auth_graphql_view)),
]
