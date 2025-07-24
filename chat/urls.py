from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import MessageListAPIview, RecentUsersView, CustomTokenObtainPairView

urlpatterns = [
    path("api/v1/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/v1/messages/<int:user_id>",
        MessageListAPIview.as_view(),
        name="GET.messages",
    ),
    path("api/recent-users/", RecentUsersView.as_view(), name="recent-users"),
]
