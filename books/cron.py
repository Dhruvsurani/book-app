import datetime

from django.db.models import Q

from books.models import RentalDetail, Book


def rent_total():

    print('\nhello')
    rent_queryset = RentalDetail.objects.filter(status='Approved')
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    for i in rent_queryset:
        rt_hr = int(i.return_time.hour)
        ct_hr = int(current_time[0:2])
        if ct_hr >= rt_hr:
            print('hello broooo')
            i.rent_hours += 1
            i.total_rent = i.total_rent + 5
            print(i.total_rent)
        i.save()
        print('rent hours ',i.rent_hours)
        print('Book rent ',i.book.book_rent)
        print('Time : ', datetime.datetime.now())



