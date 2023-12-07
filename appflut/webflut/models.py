from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
# Create your models here.


class Personal_Inform(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    SEX_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('', ''),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='')
    date_of_birth = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)

    GOAL_CHOICES = [
        ('L', 'Снижение веса'),
        ('M', 'Набор веса'),
        ('F', 'Поддержание веса'),
    ]
    goals = models.CharField(max_length=1, choices=GOAL_CHOICES, default='L')
    ACTIVE_CHOICES = [
        ('L', 'Малоактивный'),
        ('M', 'Активный'),
    ]
    active = models.CharField(max_length=1, choices=ACTIVE_CHOICES, default='L')


    class Meta:
        verbose_name = 'Личная Информация'
        verbose_name_plural = 'Личная Информация'
    def __str__(self):
        return self.user.username



class Step1Model(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.FloatField()


class StepTestModel(models.Model):
    is_male = models.BooleanField(verbose_name='Мужчина')
    is_female = models.BooleanField(verbose_name='Женщина')
class Step3Model(models.Model):
    height = models.IntegerField(default='')
    weight = models.IntegerField(default='')

class Step4Model(models.Model):
    ACTIVE_CHOICES = [
        ('L', 'малоактивный'),
        ('M', 'активный'),
    ]
    active = models.CharField(max_length=1, choices=ACTIVE_CHOICES, default='L')


class Step5Model(models.Model):
    GOAL_CHOICES = [
        ('L', 'Похудение'),
        ('M', 'Набор массы'),
        ('F', 'Поддержание веса'),
    ]
    goals = models.CharField(max_length=1, choices=GOAL_CHOICES, default='L')

class Group(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)  # Отношение "многие ко многим" с моделью User

    def __str__(self):
        return self.name



class Add_Product(models.Model):
    name = models.CharField(max_length=50)
    calories_in = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()
    class Meta:
        verbose_name = 'Продукты Все'
        verbose_name_plural = 'Продукты Все'
    def __str__(self):
        return self.name
def get_default_user():
    return User.objects.get_or_create(username='default')[0].id
class Breakfast_Products(models.Model):
    product = models.ForeignKey(Add_Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    date = models.DateTimeField(default=timezone.now)
    weight = models.FloatField(default=0)
    calories = models.FloatField(default=0)
    proteins = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    class Meta:
        verbose_name = 'Продукты Завтрака'
        verbose_name_plural = 'Продукты Завтрака'
    def __str__(self):
        return self.product.name

class Lunch_Products(models.Model):
    product = models.ForeignKey(Add_Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    date = models.DateTimeField(default=timezone.now)
    weight = models.FloatField(default=0)
    calories = models.FloatField(default=0)
    proteins = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    class Meta:
        verbose_name = 'Продукты Обеда'
        verbose_name_plural = 'Продукты Обеда'
    def __str__(self):
        return self.product.name

class Dinner_Products(models.Model):
     product = models.ForeignKey(Add_Product, on_delete=models.CASCADE)
     user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
     date = models.DateTimeField(default=timezone.now)
     weight = models.FloatField(default=0)
     calories = models.FloatField(default=0)
     proteins = models.FloatField(default=0)
     fats = models.FloatField(default=0)
     carbohydrates = models.FloatField(default=0)
     class Meta:
         verbose_name = 'Продукты Ужина'
         verbose_name_plural = 'Продукты Ужина'
     def __str__(self):
        return self.product.name




class Snack_Products(models.Model):
    product = models.ForeignKey(Add_Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    date = models.DateTimeField(default=timezone.now)
    weight = models.FloatField(default=0)
    calories = models.FloatField(default=0)
    proteins = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    class Meta:
        verbose_name = 'Продукты Перекуса'
        verbose_name_plural = 'Продукты Перекуса'
    def __str__(self):
        return self.product.name


class Activity(models.Model):
    category = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=200)
    met = models.FloatField()

    class Meta:
        verbose_name = 'Виды Активностей '
        verbose_name_plural = 'Виды Активностей'
    def __str__(self):
        return self.activity_type


class Activities_Add(models.Model):
    product = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    time = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)


class Ttime_Test(models.Model):
    name = models.TextField()
    date = models.DateTimeField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=255, choices=[('user', 'Пользователь'), ('trainer', 'Тренер')])

    def __str__(self):
        return self.user.username


class WaterConsumption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    # timestamp = models.DateTimeField(auto_now_add=True)
