from django.urls import path
from user import views


urlpatterns = [
    path('register', views.CreateUserView.as_view(), name='create_user'),
    path('login', views.LoginUserView.as_view(), name='login_user'),
]
