from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import LinkViewSet, ShortURLRedirectView, UserLinkListViewSet, RedirectView

router = DefaultRouter()
router.register(r'links', LinkViewSet, basename='link')


urlpatterns = [
    path('', include(router.urls)),
    path('user-links/', UserLinkListViewSet.as_view({'get': 'list'}), name='user-links'),
    path('redirect/<str:short_url>/', ShortURLRedirectView.as_view(), name='redirect'),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

# /api/auth/login/ - Залогинить пользователя, получить токен. POST запрос с username и password