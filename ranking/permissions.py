from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # if obj.status == "public":
            #     return True
            # else: 
            #     if obj.author == request.user:
            #         return False
            #     else:
            #         return False
            return True

        return obj.author == request.user