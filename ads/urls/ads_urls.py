from django.urls import path
import ads.views

urlpatterns = [
    path('', ads.views.AdsListView.as_view(), name="all_ads"),
    path('<int:pk>', ads.views.AdDetailView.as_view(), name="ad"),
    path('<int:pk>/update/', ads.views.AdUpdateView.as_view()),
    path('<int:pk>/delete/', ads.views.AdDeleteView.as_view()),
    path('<int:pk>/upload_image/', ads.views.AdImageView.as_view()),
    path('create/', ads.views.AdCreateView.as_view()),
]
