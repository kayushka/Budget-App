from django import forms
from django.contrib.auth.forms import UserCreationForm

from noname.models import INCOME_CHOICES, EXPENSES_CHOICES, MyUser


class AddIncomeForm(forms.Form):
    category = forms.ChoiceField(label="kategoria", choices=INCOME_CHOICES)
    amount = forms.FloatField(label="kwota")
    comment = forms.CharField(widget=forms.Textarea, label="komentarz")


class AddExpensesForm(forms.Form):
    category = forms.ChoiceField(label="kategoria", choices=EXPENSES_CHOICES)
    amount = forms.FloatField(label="kwota")
    comment = forms.CharField(widget=forms.Textarea, label="komentarz")


class UserCreationForm2(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser