from rest_framework import viewsets, status
from rest_framework.views import APIView
from .permissions import IsAdminOrCreateOnly
from .models import Link
from .serializers import LinkSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from rest_framework.permissions import AllowAny, IsAdminUser

class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all().order_by('-created_at')
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
            links = Link.objects.filter(user=user).order_by('-created_at')
            user_data = {
                'id': user.id,
                'username': user.username,
                'links': LinkSerializer(links, many=True).data
            }
            data.append(user_data)
        return Response(data)


class ShortURLRedirectView(RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        short_url = self.kwargs.get('short_url')
        link = get_object_or_404(Link, short_url=short_url, is_active=True)
        Link.objects.increment_clicks(short_url)  # Увеличиваем количество кликов
        return link.url

class AdminCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserDeleteView(APIView):
    permission_classes = [IsAdminUser] 

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)