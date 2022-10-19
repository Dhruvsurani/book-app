from django.urls import path
from .views import BookCreateView, BookListView, BookDetailView, RentBookView, UserRentedBookListView, BookUpdateView, \
    BookDeleteView, ReturnBookView, RentRequestView, RentRequestUpdateView, RequestDeleteView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('book/create/', BookCreateView.as_view(), name='book_create'),
    path('book/<slug:slug>', BookDetailView.as_view(), name='book-detail'),
    path('<slug:slug>/update', BookUpdateView.as_view(), name='book-update'),
    path('delete', BookDeleteView.as_view(), name='book-delete'),
    path('delete_request/<int:pk>/', RequestDeleteView.as_view(), name='request-delete'),
    path('rent_book', RentBookView.as_view(), name='rent-book'),
    path('rented_books', UserRentedBookListView.as_view(), name='rented-booklist'),
    path('return_book/<int:pk>', ReturnBookView.as_view(), name='return-book'),
    path('rent_request_list', RentRequestView.as_view(), name='rent-requestlist'),
    path('rent_request_list/<int:pk>', RentRequestUpdateView.as_view(), name='return-bookupdate'),
    # path('rent_update/<int:pk>', BookUpdateView.as_view(), name='rent-update')
]
