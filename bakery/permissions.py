from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """
    Custom permission to only allow users with manager role to perform certain actions.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
            
        # Check if the user has staff status (simplified manager check)
        # In a real application, you might have a more complex role system
        return request.user.is_staff