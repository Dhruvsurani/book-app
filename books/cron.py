from books.models import RentalDetail, Book


def rent_total():

    print('\nhello')
    rent_queryset = RentalDetail.objects.filter(return_time=None)

    for i in rent_queryset:
        i.rent_hours += 1
        i.total_rent = i.book.book_rent * i.rent_hours
        i.save()
        print('rent hours ',i.rent_hours)
        print('Book rent ',i.book.book_rent)



