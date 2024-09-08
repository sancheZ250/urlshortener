from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Link

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'url', 'short_url', 'clicks', 'created_at', 'is_active']
        read_only_fields = ['short_url', 'clicks', 'created_at', 'user']