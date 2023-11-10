from django import forms
from django.contrib.auth.models import User
from .models import Personal_Inform, Add_Product, Step1Model, Step3Model, Step4Model, Step5Model, StepTestModel
from django.core.exceptions import ValidationError

class DateForm(forms.Form):
    date = forms.DateField()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    username = forms.CharField(label='Username', max_length=None)
    #user_type = forms.ChoiceField(choices=(('user', 'Пользователь'), ('trainer', 'Тренер')), widget=forms.RadioSelect)
    user_type = forms.ChoiceField(choices=(('user', 'Пользователь'), ('trainer', 'Тренер')),
    widget=forms.RadioSelect(attrs={'class': 'form_toggle-radio'}))

    def validate_username(self, value):
        if not value:
            raise ValidationError("тестовая валидация")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        self.validate_username(username)
        return username
    class Meta:
        model = User
        fields = ('username', 'password', 'user_type',)

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Passwords don\'t match.')
    #     return cd['password2']


class PersonalInformForm(forms.ModelForm):
    class Meta:
        model = Personal_Inform
        fields = ['weight', 'height', 'sex', 'first_name', 'last_name', 'date_of_birth',  'goals', 'active',]

class Step1Form(forms.ModelForm):
    class Meta:
        model = Step1Model
        fields = ['first_name', 'last_name', 'date_of_birth']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилию'}),
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'Полных лет'}),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'date_of_birth': '',
        }


class StepTestForm(forms.ModelForm):
    class Meta:
        model = StepTestModel
        fields = ['is_male', 'is_female']
class Step3Form(forms.ModelForm):
    class Meta:
        model = Step3Model
        fields = ['height', 'weight']
        widgets = {
            'height': forms.TextInput(attrs={'placeholder': 'Рост, см'}),
            'weight': forms.TextInput(attrs={'placeholder': 'Вес, кг'}),
        }
        labels = {
            'height': '',
            'weight': '',
        }



class AddProductForm(forms.ModelForm):
    class Meta:
        model = Add_Product
        fields = ['name', 'calories_in', 'proteins', 'fats', 'carbohydrates',]
