from rest_framework import permissions


class IsOwnerOfMovieOrStaffPermission(permissions.BasePermission):
    """
    Checks if the user is the owner of the movie object.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.user == request.user or request.user.is_staff == True


