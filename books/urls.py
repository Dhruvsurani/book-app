from django.urls import path
from .views import BookCreateView, BookListView, BookDetailView, RentBookView, UserRentedBookListView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('book/create/', BookCreateView.as_view(), name='book_create'),
    path('book/<slug:slug>', BookDetailView.as_view(), name='book-detail'),
    path('<slug:slug>/update', BookUpdateView.as_view(), name='book-update'),
    path('delete', BookDeleteView.as_view(), name='book-delete'),
    path('rent_book', RentBookView.as_view(), name='rent-book'),
    path('rented_books', UserRentedBookListView.as_view(), name='rented-booklist'),
    # path('rent_update/<int:pk>', BookUpdateView.as_view(), name='rent-update')
]
