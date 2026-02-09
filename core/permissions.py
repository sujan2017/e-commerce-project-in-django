from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'role') and
            request.user.role.role == "ADMIN"
        )


class IsDelivery(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'role') and
            request.user.role.role == "DELIVERY"
        )

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'role') and
            request.user.role.role == "CUSTOMER"
        )


class IsSupplier(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'role') and
            request.user.role.role == "SUPPLIER"
        )