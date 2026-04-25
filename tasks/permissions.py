from rest_framework import permissions


class ProjectOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
               or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user



class TaskPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        is_owner = (obj.project.created_by == request.user)
        is_creator = (obj.creator == request.user)
        is_executor = (obj.executor == request.user)

        if request.method in ("PUT", "PATCH"):
            return is_owner or is_creator or is_executor
        if request.method == "DELETE":
            return is_owner or is_creator

        return False



class CommentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        is_owner = (obj.task.project.created_by == request.user)
        is_author = (obj.author == request.user)

        if request.method in ("PUT", "PATCH"):
            return is_author

        if request.method == "DELETE":
            return is_author or is_owner

        return False