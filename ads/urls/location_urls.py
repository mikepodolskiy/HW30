from django.urls import path
import ads.views

urlpatterns = [
        path('create/', ads.views.UserCreateView.as_view()),
    ]