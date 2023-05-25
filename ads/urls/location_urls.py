from django.urls import path
import ads.views

urlpatterns = [
        path('', ads.views.LocationListView.as_view()),
        path('<int:pk>/', ads.views.LocationDetailView.as_view()),
        path('create/', ads.views.LocationCreateView.as_view()),
        path('<int:pk>/update/', ads.views.LocationUpdateView.as_view()),
        path('<int:pk>/delete/', ads.views.LocationDeleteView.as_view()),
    ]