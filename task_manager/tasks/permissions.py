from rest_framework.permissions import BasePermission
 
 
# IsAuthenticated (built-in) just checks: is this user logged in?
# IsOwner (ours) goes one step further: does this user OWN this object?
 
# If we only used IsAuthenticated, user A could edit user B's tasks
# IsOwner prevents that — it checks the task's owner field
 
class IsOwner(BasePermission):
 
    # This message shows in the API response when permission is denied
    message = "You do not have permission to access this task."
 
    def has_object_permission(self, request, view, obj):
        # obj = the Task being accessed
        # request.user = who is making the request
        # Return True only if they match
        return obj.owner == request.user