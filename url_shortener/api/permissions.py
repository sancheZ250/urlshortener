from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrCreateOnly(BasePermission):
    """
    Разрешение, позволяющее создавать ссылки всем пользователям,
    но редактировать и удалять только администраторам.
    """
    def has_permission(self, request, view):
        # Разрешить доступ для всех пользователей для GET, HEAD, OPTIONS методов
        if request.method in SAFE_METHODS or request.method == 'POST':
            return True
        
        # Разрешить доступ только администраторам для PUT, PATCH, DELETE методов
        return request.user and request.user.is_staff