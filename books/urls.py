from django.urls import path
from .views import BookCreateView, BookListView, BookDetailView

urlpatterns = [
    path('book/create/', BookCreateView.as_view(), name='book_create'),
    path('', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book-detail'),
]