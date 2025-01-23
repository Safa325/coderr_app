from rest_framework.permissions import BasePermission
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, SAFE_METHODS
 
class IsOwnerOrAdminPermission(BasePermission):
    """
    Gewährt Zugriff nur, wenn der Benutzer der Besitzer eines Objekts oder ein Admin ist.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_staff

class IsBusinessUser(BasePermission):
    """
    Permission to check if the user is a business user.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        profile = getattr(request.user, 'profile', None)
        return profile and profile.type == 'business'

class IsCustomerUser(BasePermission):
    """
    Permission to check if the user is a customer user.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        profile = getattr(request.user, 'profile', None)
        return profile and profile.type == 'customer'
    
class OrderPermissions(BasePermission):
    """
    Custom permission to allow:
    - Customers to create (POST) orders
    - Business users to update (PATCH) orders
    - Admins to delete (DELETE) orders
    - Any authenticated user to read (GET) orders
    """
    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)

        if request.method == 'POST':
            return profile and profile.type == 'customer'

        if request.method == 'PATCH':
            return profile and profile.type == 'business'
        
        if request.method == 'DELETE':
            return request.user.is_staff 

        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        return False

   
    
   






