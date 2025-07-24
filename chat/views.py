from django.shortcuts import render
from rest_framework import views, response, permissions
from .models import Messages, User
from .serializers import MessageSerializer, RecentUserSerializer, CustomTokenObtainPairSerializer
from django.db.models import Q, Max
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
class MessageListAPIview(views.APIView):
    def get(self, request, user_id):
        other_user = User.objects.get(id=user_id)
        messages = Messages.objects.filter(
            sender__in=[request.user, other_user],
            receiver__in=[request.user, other_user],
        ).order_by("timestamp")
        return response.Response(MessageSerializer(messages, many=True).data)


class RecentUsersView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get messages where user is either sender or receiver
        messages = Messages.objects.filter(Q(sender=user) | Q(receiver=user))

        # Get unique users and annotate with latest timestamp for ordering
        latest_map = (
            messages.values("sender", "receiver")
            .annotate(latest=Max("timestamp"))
            .order_by("-latest")
        )

        seen_user_ids = set()
        recent_users = []

        for entry in latest_map:
            sender_id = entry["sender"]
            receiver_id = entry["receiver"]
            partner_id = receiver_id if sender_id == user.id else sender_id

            if partner_id not in seen_user_ids and partner_id != user.id:
                try:
                    partner = User.objects.get(id=partner_id)
                    recent_users.append(partner)
                    seen_user_ids.add(partner_id)
                except User.DoesNotExist:
                    continue

        serializer = RecentUserSerializer(recent_users, many=True)
        return response.Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer