from rest_framework import permissions

class ModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            return True
        
        if user.is_superuser:
            return True
        
        return user.groups.filter(name='Moderator').exists()
