from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """
        The methods should
            either return 'True' or 'False' otherwise.
            
        In our cases, the one we're doing is
            "Has this user enrolled in this course" ?
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()