from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
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


class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'


class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book_list'

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

    def post(self, request, *args, **kwargs):
        form = RentBookForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            book = Book.objects.get(title=form.cleaned_data['book'])
            book.rented_users.add(request.user)
            if book.total_copies == 0:
                pass
            else:
                book.total_copies -= 1
                book.save()
                return HttpResponseRedirect(reverse_lazy('book_list'))

        return HttpResponseRedirect(reverse_lazy('book_list'))


class UserRentedBookListView(ListView):
    model = RentalDetail
    template_name = 'books/rented_user_list.html'
    context_object_name = 'rented_book'
    paginate_by = 5

    # def get_queryset(self, *args, **kwargs):
    #     user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     return RentalDetail.objects.get(user=user).order_by('-date_posted')
# class BookUpdateView(UpdateView):
#     model = RentalDetail
#     fields = ['penalty']
#     slug_field = 'id'
#     template_name = 'books/book_detail.html'
#
#     def post(self, request, *args, **kwargs):
#         rent = Book.objects.filter(title=request.POST['title'])
#         print(rent.book_rent)
#         RentalDetail.objects.filter(username=request.POST['username']).update(penalty=2)
#     # def get_object(self, queryset=None):
#     #     rent = self.
#     # # RentalDetail.penalty = RentalDetail.penalty + Book.book_ren