# chat/serializers.py

from rest_framework import serializers
from .models import Messages, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)
    receiver_name = serializers.CharField(source="receiver.full_name", read_only=True)

    class Meta:
        model = Messages
        fields = ["id", "sender", "sender_name", "receiver", "receiver_name", "content", "timestamp"]


class RecentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email']
        

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom fields from the user object
        data['id'] = self.user.id
        data['full_name'] = {self.user.full_name}
        return data
