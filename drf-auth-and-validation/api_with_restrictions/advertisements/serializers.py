from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import Advertisement

class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)

class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user = self.context['request'].user


        if not self.instance or data.get('status') == 'OPEN':

            open_ads_count = Advertisement.objects.filter(creator=user, status='OPEN').count()
            if open_ads_count >= 10:
                raise serializers.ValidationError(f'User  {user} can\'t create more than 10 open items!')

        return data

    def update(self, instance, validated_data):
        """Метод для обновления"""

        self.validate(validated_data)
        return super().update(instance, validated_data)
