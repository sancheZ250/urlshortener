from rest_framework import serializers
from .models import Link

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'url', 'short_url', 'clicks', 'date_created', 'is_active', 'user']
        read_only_fields = ['short_url', 'clicks', 'date_created', 'user']