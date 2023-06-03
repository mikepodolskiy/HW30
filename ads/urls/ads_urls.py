from django.urls import path
import ads.views

urlpatterns = [
    path('', ads.views.AdsListView.as_view(), name="all_ads"),
    path('<int:pk>/', ads.views.AdDetailView.as_view(), name="ad"),
    path('<int:pk>/update/', ads.views.AdUpdateView.as_view()),
    path('<int:pk>/delete/', ads.views.AdDeleteView.as_view()),
    path('<int:pk>/upload_image/', ads.views.AdImageView.as_view()),
    path('create/', ads.views.AdCreateView.as_view()),
    path('set/', ads.views.AdsSetListView.as_view()),
    path('set/<int:pk>/', ads.views.AdsSetDetailView.as_view()),
    path('set/<int:pk>/update/', ads.views.AdsSetUpdateView.as_view()),
    path('set/<int:pk>/delete/', ads.views.AdsSetDeleteView.as_view()),
    path('set/create/', ads.views.AdsSetCreateView.as_view()),
]
