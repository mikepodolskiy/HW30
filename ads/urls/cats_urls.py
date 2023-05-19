from django.urls import path
import ads.views

urlpatterns = [
    path('', ads.views.CategoriesListView.as_view(), name="all_categories"),
    path('create/', ads.views.CategoryCreateView.as_view()),
    path('<int:pk>', ads.views.CategoryDetailView.as_view(), name="category"),
    path('<int:pk>/update/', ads.views.CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', ads.views.CategoryDeleteView.as_view()),
]
