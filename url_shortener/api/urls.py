from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import LinkViewSet, ShortURLRedirectView, UserDeleteView, UserLinkListViewSet, RedirectView, AdminCheckView

router = DefaultRouter()
router.register(r'links', LinkViewSet, basename='link')


urlpatterns = [
    path('', include(router.urls)),
    path('user-links/', UserLinkListViewSet.as_view({'get': 'list'}), name='user-links'),
    path('redirect/<str:short_url>/', ShortURLRedirectView.as_view(), name='redirect'),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('is-admin/', AdminCheckView.as_view(), name='is_admin'),
    path('users/<int:user_id>/delete/', UserDeleteView.as_view(), name='user-delete'),
]

# /api/auth/login/ - Залогинить пользователя, получить токен. POST запрос с username и password