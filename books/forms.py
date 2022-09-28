from django import forms
from .models import RentalDetail


class RentBookForm(forms.ModelForm):

    class Meta:
        model = RentalDetail
        fields = ['user', 'book']
