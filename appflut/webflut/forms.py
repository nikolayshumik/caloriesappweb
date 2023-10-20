from django import forms
from django.contrib.auth.models import User
from .models import Personal_Inform, Add_Product


class DateForm(forms.Form):
    date = forms.DateField()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('username','email',)

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Passwords don\'t match.')
    #     return cd['password2']


class PersonalInformForm(forms.ModelForm):
    class Meta:
        model = Personal_Inform
        fields = ['sex', 'date_of_birth', 'weight', 'height', 'goals', 'active',]


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Add_Product
        fields = ['name', 'calories_in', 'proteins', 'fats', 'carbohydrates',]
