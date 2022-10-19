import datetime

from django.db.models import Q

from books.models import RentalDetail, Book


def rent_total():

    print('\nhello')
    rent_queryset = RentalDetail.objects.filter(status='Approved')

    for i in rent_queryset:
        print(i.issue_date)
        print(i.issue_date.hour)
        print(i.issue_date.time)
        if i.return_time is not None:
            hr_total = i.return_time.hour - i.issue_date.hour
            if hr_total > i.rent_hours:
                i.rent_hours += 1
                i.total_rent = i.total_rent + 5
            print(hr_total)

        i.save()
        print('rent hours ',i.rent_hours)
        print('Book rent ',i.book.book_rent)
        print('Time : ', datetime.datetime.now())



