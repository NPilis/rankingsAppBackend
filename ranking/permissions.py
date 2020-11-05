from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

class IsOwnerOfRanking(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsOwnerOfPosition(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.ranking.author == request.user

class IsAccesableForCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.status == "private":
            print(request.user)
            if obj.author == request.user:
                return True
            else:
                return False
        else:
            return True