from django.db.models import Q

from books.models import RentalDetail, Book


def rent_total():

    print('\nhello')
    rent_queryset = RentalDetail.objects.filter(Q(return_time=None) & Q(status='Approved'))

    for i in rent_queryset:
        i.rent_hours += 1
        i.total_rent = i.book.book_rent * i.rent_hours
        i.save()
        print('rent hours ',i.rent_hours)
        print('Book rent ',i.book.book_rent)



