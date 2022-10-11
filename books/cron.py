import datetime

from django.db.models import Q

from books.models import RentalDetail, Book


def rent_total():

    print('\nhello')
    rent_queryset = RentalDetail.objects.filter(Q(return_time=None) & Q(status='Approved'))

    for i in rent_queryset:
        i.rent_hours += 1
        if i.rent_hours > 2:
            i.total_rent = i.total_rent + 5
        i.save()
        print('rent hours ',i.rent_hours)
        print('Book rent ',i.book.book_rent)
        print('Time : ', datetime.datetime.now())



