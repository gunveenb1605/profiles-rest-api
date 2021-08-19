from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile only"""

    #For each request , it will chekc if authorized person is trying to update info
    def has_object_permission(self, request, view, obj):
        """Check if user is trying to edit their own profile"""

        #first check if it is a safe method, eg. GET request. POST, PUT, PATCH is not safe method
        if request.method in permissions.SAFE_METHODS:
            return True

        #if it is not a safe method, check if they are authorized to make change. Django will attach the profile of the authenticated user
        #if that profile, matches the one that is being updated, then it is okay
        return obj.id == request.user.id
