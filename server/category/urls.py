from django.urls import path
from category import views


urlpatterns = [
    path('', views.CreateListCategoryView.as_view(),
         name='create_list_category'),
]
