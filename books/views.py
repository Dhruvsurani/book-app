import datetime

from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Book, RentalDetail
from .forms import RentBookForm
from asgiref.sync import async_to_sync

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


class BookUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
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


class BookDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Book
    success_url = '/'


class BookListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Book
    context_object_name = 'book_list'
    extra_context = {'room_name': 'book-list'}


class BookDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
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


# def roundTime(dt):
#
#     if dt.minute >= 30:
#         dt1 = dt.replace(minute=00)
#         h = dt.hour + 1
#         dt2 = dt1.replace(hour=h)
#     else:
#         dt2 = dt.replace(minute=00)
#     return dt2
def roundTime(dt=None, roundTo=60):
    """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
    if dt == None: dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


class RentBookView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = 'books/book_detail.html'
    model = RentalDetail
    fields = [
        'user',
        'book',
        'rent_hours',
    ]
    success_url = reverse_lazy('book_list')
    extra_context = {'room_name': 'book-rent'}

    def post(self, request, *args, **kwargs):
        form = RentBookForm(request.POST)
        if form.is_valid():

            obj = form.save()
            book = Book.objects.get(title=form.cleaned_data['book'])
            book.rented_users.add(request.user)
            obj.total_rent = book.book_rent * obj.rent_hours
            obj.save()

            current_user = request.user
            channel_layer = get_channel_layer()
            data = f"{current_user} is requesting for {book}"
            async_to_sync(channel_layer.group_send)(
                str('notification_request'),  # Channel Name, Should always be string
                {
                    "type": "notify",  # Custom Function written in the consumers.py
                    "text": data,
                },
            )
            if book.total_copies == 0:
                pass
            else:
                book.total_copies -= 1
                book.save()
                return HttpResponseRedirect(reverse_lazy('book_list'))

        return HttpResponseRedirect(reverse_lazy('book_list'))


class ReturnBookView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = RentalDetail
    fields = [
        'return_time'
    ]
    extra_context = {'room_name': 'book-return'}

    def post(self, request, *args, **kwargs):
        title = RentalDetail.objects.get(id=request.POST['book_id'])
        # breakpoint()
        RentalDetail.objects.filter(id=title.id).update(status='Returned', return_time=roundTime(datetime.datetime.now(), roundTo=60 * 60))
        # rent = RentalDetail.objects.filter(id=request.POST['book_id'])
        # now = datetime.datetime.now()
        # title.return_time = roundTime(now, roundTo=60 * 60)
        book = title.book.id
        rented_user = Book.objects.get(id=book)
        rented_user.rented_users.remove(request.user)
        rented_user.total_copies += 1
        rented_user.save()
        # title.save()
        return HttpResponseRedirect(reverse_lazy('rented-booklist'))


class RequestDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = RentalDetail
    success_url = '/'


class UserRentedBookListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = RentalDetail
    template_name = 'books/rented_user_list.html'
    context_object_name = 'rented_book'
    # ordering = ['-issue_date']

    extra_context = {'room_name': 'book-rentlist'}

    def get_queryset(self):
        return RentalDetail.objects.filter(Q(user=self.request.user) & Q(status='Approved') | Q(status='Returned')).order_by('-id')




class RentRequestView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = RentalDetail
    context_object_name = 'rent_request'
    template_name = 'books/rent_request_list.html'
    extra_context = {'room_name': 'book-rent-requests'}

    def get_queryset(self):
        return RentalDetail.objects.all().order_by('-id')


class RentRequestUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = RentalDetail
    fields = [
        'status'
    ]
    extra_context = {'room_name': 'book-rent-approved'}

    def post(self, request, *args, **kwargs):
        RentalDetail.objects.filter(id=request.POST['book_id']).update(status='Approved')
        rented = RentalDetail.objects.filter(issue_date=None)
        for i in rented:
            if i.status == 'Approved':
                i.issue_date = roundTime(datetime.datetime.now(), roundTo=60 * 60)
                i.save()
        return HttpResponseRedirect(reverse_lazy('rent-requestlist'))