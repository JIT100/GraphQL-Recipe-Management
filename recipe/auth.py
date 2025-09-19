from functools import wraps
from typing import Callable

from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    """Strawberry permission that allows only authenticated Django users."""
    message = "<h1> Authentication required. Kindly Login via the /api/token/ endpoint.</h1>"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        request = info.context.get('request')
        return bool(request and getattr(request, 'user', None) and request.user.is_authenticated)
