from django.urls import path
from .views import BookCreateView, BookListView, BookDetailView, RentBookView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('book/create/', BookCreateView.as_view(), name='book_create'),
    path('book/<slug:slug>', BookDetailView.as_view(), name='book-detail'),
    path('rent_book', RentBookView.as_view(), name='rent-book'),
]
