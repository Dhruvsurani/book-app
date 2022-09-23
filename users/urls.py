from django.urls import path
from .views import IndexView, SignUpView, HomeView, CustomLoginView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
]