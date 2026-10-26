from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    """
    Anyone can read a post.
    Only its author can edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Anyone can read
        if request.method in SAFE_METHODS:
            return True
        
        # Only the author can modify/delete
        return obj.author == request.user