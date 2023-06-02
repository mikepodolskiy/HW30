from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import authentication.views

urlpatterns = [
    path('', authentication.views.UserListView.as_view(), name="all_users"),
    path('<int:pk>/', authentication.views.UserDetailView.as_view(), name="user"),
    path('<int:pk>/update/', authentication.views.UserUpdateView.as_view()),
    path('<int:pk>/delete/', authentication.views.UserDeleteView.as_view()),
    path('create/', authentication.views.UserCreateView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
