from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to create, edit, or delete objects.
    Other users can only view (read) objects.
    """

    def has_permission(self, request, view):
        # Allow read-only methods (GET, HEAD, OPTIONS) for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow write permissions only for admin users
        return request.user and request.user.is_staff