from django import forms
from django.contrib.auth.models import User
from .models import Personal_Inform, Add_Product, Step1Model, Step2Model, Step3Model


class DateForm(forms.Form):
    date = forms.DateField()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=[('user', 'Пользователь'), ('trainer', 'Тренер')])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'user_type',)

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Passwords don\'t match.')
    #     return cd['password2']


class PersonalInformForm(forms.ModelForm):
    class Meta:
        model = Personal_Inform
        fields = ['sex', 'first_name', 'last_name', 'date_of_birth', 'weight', 'height', 'goals', 'active',]

class Step1Form(forms.ModelForm):
    class Meta:
        model = Step1Model
        fields = ['first_name', 'last_name', 'date_of_birth']

class Step2Form(forms.ModelForm):
    class Meta:
        model = Step2Model
        fields = ['sex']

class Step3Form(forms.ModelForm):
    class Meta:
        model = Step3Model
        fields = ['height', 'weight']


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Add_Product
        fields = ['name', 'calories_in', 'proteins', 'fats', 'carbohydrates',]
