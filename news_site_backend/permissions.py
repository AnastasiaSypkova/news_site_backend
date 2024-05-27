from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnly(BasePermission):
    """
    Grant read only permission
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsSuperUser(BasePermission):
    """
    Grant superuser permission
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class UpdateOwnProfile(BasePermission):
    """
    Grant permission to update own profile
    """

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.id == request.user.id
        else:
            return False


class EditeOwnObject(BasePermission):
    """
    Grant user permission to edit or delete its own news/comments
    """

    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj.author.id == request.user.id
        else:
            return False
