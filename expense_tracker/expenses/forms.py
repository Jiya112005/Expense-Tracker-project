from django import forms
from .models import Expense
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class ExpenseListForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title','category','amount','date']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model=User
        fields = ['username','email','password','password2']