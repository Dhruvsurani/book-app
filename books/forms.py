from django import forms
from .models import RentalDetail


class RentBookForm(forms.ModelForm):

    class Meta:
        model = RentalDetail
        fields = ['user', 'book', 'rent_hours']


# class RentUpdateForm(forms.ModelForm):
#
#     def save(self, commit=True):
#         if self.instance.pk == None:
#             self.instance.rent =
