import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Book, RentalDetail
from .forms import RentBookForm

# Create your views here.tai


class BookCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = 'books/form.html'
    model = Book
    fields = [
        'title',
        'author',
        'summary',
        'isbn',
        'book_rent',
        'total_copies'
    ]
    success_url = reverse_lazy('book_create')
    extra_context = {'room_name': 'book-create'}


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'books/form.html'
    fields = [
        'title',
        'author',
        'summary',
        'isbn',
        'book_rent',
        'total_copies'

    ]
    success_url = '/'
    extra_context = {'room_name': 'book-update'}


class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'


class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'
    extra_context = {'room_name': 'book-list'}


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book_list'
    extra_context = {'room_name': 'book-details'}

    def get_context_data(self, **kwargs):
        context = {}
        form = RentBookForm()
        if self.object:
            context['form'] = form
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)


class RentBookView(CreateView):
    template_name = 'books/book_detail.html'
    model = RentalDetail
    fields = [
        'user',
        'book'
    ]
    success_url = reverse_lazy('book_list')
    extra_context = {'room_name': 'book-rent'}

    def post(self, request, *args, **kwargs):
        form = RentBookForm(request.POST)
        if form.is_valid():
            obj = form.save()
            book = Book.objects.get(title=form.cleaned_data['book'])
            book.rented_users.add(request.user)
            obj.total_rent = book.book_rent
            obj.save()
            if book.total_copies == 0:
                pass
            else:
                book.total_copies -= 1
                book.save()
                return HttpResponseRedirect(reverse_lazy('book_list'))

        return HttpResponseRedirect(reverse_lazy('book_list'))


class ReturnBookView(UpdateView):
    model = RentalDetail
    fields = [
        'return_time'
    ]
    extra_context = {'room_name': 'book-return'}

    def post(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        RentalDetail.objects.filter(id=request.POST['book_id']).update(return_time= roundTime(now, roundTo=60 * 60))
        title = RentalDetail.objects.get(id=request.POST['book_id'])
        book = title.book.id
        rented_user = Book.objects.get(id=book)
        rented_user.rented_users.remove(request.user)
        rented_user.total_copies += 1
        rented_user.save()
        return HttpResponseRedirect(reverse_lazy('rented-booklist'))


class UserRentedBookListView(ListView):
    model = RentalDetail
    template_name = 'books/rented_user_list.html'
    context_object_name = 'rented_book'

    extra_context = {'room_name': 'book-rentlist'}
    def get_queryset(self):
        return RentalDetail.objects.filter(Q(user=self.request.user) & Q(status='Approved'))


class RentRequestView(ListView):
    model = RentalDetail
    context_object_name = 'rent_request'
    template_name = 'books/rent_request_list.html'
    extra_context = {'room_name': 'book-rent-requests'}

    def get_queryset(self):
        return RentalDetail.objects.all()


def roundTime(dt=None, roundTo=60):
    if dt is None:
        dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


class RentRequestUpdateView(UpdateView):
    model = RentalDetail
    fields = [
        'status'
    ]
    extra_context = {'room_name': 'book-rent-approved'}

    def post(self, request, *args, **kwargs):
        RentalDetail.objects.filter(id=request.POST['book_id']).update(status='Approved')
        rented = RentalDetail.objects.filter(issue_time=None)
        for i in rented:
            if i.status == 'Approved':
                i.issue_time = roundTime(datetime.datetime.now(), roundTo=60 * 60)
                i.save()
        return HttpResponseRedirect(reverse_lazy('rent-requestlist'))