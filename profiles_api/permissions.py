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


#For users to be only able to update their own feed items
class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id
