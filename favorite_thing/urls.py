from django.urls import path
from favorite_thing import views

urlpatterns = [
    path('', views.FavoriteThingsList.as_view(), name='favorite-thing'),
    path('<int:pk>', views.FavoriteThingsDetails.as_view(), name='favorite-thing-detail'),
    path('categories/<int:category_id>', views.FavoriteThingsInCategory.as_view(), name='favorite-things-category')
]
