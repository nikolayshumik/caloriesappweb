from django import forms
from django.contrib.auth.models import User
from .models import Personal_Inform, Add_Product, Step1Model, Step3Model, Step4Model, Step5Model, StepTestModel
from django.core.exceptions import ValidationError


class DateForm(forms.Form):
    date = forms.DateField()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    username = forms.CharField(label='Логин', max_length=30)
    user_type = forms.ChoiceField(choices=(('user', 'Пользователь'), ('trainer', 'Тренер')),
                                  widget=forms.RadioSelect(attrs={'class': 'form_toggle-radio'}),
                                  label='Тип')

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
        fields = ['weight', 'height', 'sex', 'date_of_birth', 'goals', 'active', ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'min': '1924-01-01'})
        }


    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight < 1 or weight > 240:
            raise forms.ValidationError('Вес должен быть числом от 1 до 240')
        return weight

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height < 1 or height > 240:
            raise forms.ValidationError('Рост должен быть числом от 1 до 240')
        return height

    # def clean_date_of_birth(self):
    #     date_of_birth = self.cleaned_data.get('date_of_birth')
    #     if date_of_birth <= 0:
    #         raise forms.ValidationError('Возраст должен быть положительным числом')
    #     return date_of_birth


class Step1Form(forms.ModelForm):
    class Meta:
        model = Step1Model
        fields = ['first_name', 'last_name', 'date_of_birth']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилию'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
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
        fields = ['name', 'calories_in', 'proteins', 'fats', 'carbohydrates', ]
        labels = {
            'name': 'Название продукта',
            'calories_in': 'ккал',
            'proteins': 'Б',
            'fats': 'Ж',
            'carbohydrates': 'У',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        proteins = self.cleaned_data.get('proteins')
        fats = self.cleaned_data.get('fats')
        carbohydrates = self.cleaned_data.get('carbohydrates')
        calories = proteins * 4 + fats * 9 + carbohydrates * 4
        instance.calories_in = calories

        if commit:
            instance.save()
        return instance
