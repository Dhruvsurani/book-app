import datetime

from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.
def roundTime(dt=None, roundTo=60):
    if dt is None:
        dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, help_text="description of the book")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character ISBN number')
    slug = models.SlugField(max_length=100, unique=True)
    book_rent = models.IntegerField()
    publish_date = models.DateTimeField(default=timezone.now)
    total_copies = models.IntegerField()
    rented_users = models.ManyToManyField(User, related_name='rented_user')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.isbn
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'slug': self.slug})


class RentalDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_name')
    rent_hours = models.FloatField(default=0)
    issue_time = models.TimeField()
    return_time = models.TimeField(null=True)
    total_rent = models.IntegerField(default=0)
    status_choices = (('Approved', 'Approved'),
                      ('Not Approved', 'Not Approved'),
                      )
    status = models.CharField(max_length=100, choices=status_choices, default='Not Approved')

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.issue_time = roundTime(datetime.datetime.now(), roundTo=60 * 60)

        return super().save(*args, **kwargs)
