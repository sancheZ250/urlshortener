from rest_framework import viewsets

from .permissions import IsAdminOrCreateOnly
from .models import Link
from .serializers import LinkSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAdminOrCreateOnly]

    def perform_create(self, serializer):
        # Извлекаем URL из сериализатора
        url = serializer.validated_data['url']
        
        # Генерируем короткий URL
        link = Link.objects.create_short_url(url, self.request.user)

class UserLinkListViewSet(viewsets.ViewSet):
    def list(self, request):
        users = User.objects.all()
        data = []
        for user in users:
            links = Link.objects.filter(user=user)
            user_data = {
                'username': user.username,
                'links': LinkSerializer(links, many=True).data
            }
            data.append(user_data)
        return Response(data)


class ShortURLRedirectView(RedirectView):
    permanent = False  # Не обязательно постоянное перенаправление
    query_string = False  # Не сохранять параметры запроса

    def get_redirect_url(self, *args, **kwargs):
        short_url = self.kwargs.get('short_url')
        link = get_object_or_404(Link, short_url=short_url, is_active=True)
        Link.objects.increment_clicks(short_url)  # Увеличиваем количество кликов
        return link.url
