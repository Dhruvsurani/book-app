from django.urls import path, include
from .views import SignUpView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', include('books.urls')),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]