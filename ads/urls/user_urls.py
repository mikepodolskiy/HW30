from django.urls import path
import ads.views

urlpatterns = [
    path('', ads.views.UserListView.as_view(), name="all_users"),
    path('<int:pk>/', ads.views.UserDetailView.as_view(), name="user"),
    path('<int:pk>/update/', ads.views.UserUpdateView.as_view()),
    path('<int:pk>/delete/', ads.views.UserDeleteView.as_view()),
    path('create/', ads.views.UserCreateView.as_view()),
]
