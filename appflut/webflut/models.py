from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
# Create your models here.


class Personal_Inform(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line
    SEX_CHOICES = [
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='M')
    date_of_birth = models.FloatField()
    weight = models.FloatField()
    height = models.FloatField()

    GOAL_CHOICES = [
        ('L', 'Похудение'),
        ('M', 'Набор массы'),
        ('F', 'Поддержание веса'),
    ]
    goals = models.CharField(max_length=1, choices=GOAL_CHOICES, default='L')
    ACTIVE_CHOICES = [
        ('L', 'Низкая активность'),
        ('M', 'Средняя активность'),
        ('H', 'Высокая активность'),
    ]
    active = models.CharField(max_length=1, choices=ACTIVE_CHOICES, default='L')


    class Meta:
        verbose_name = 'Личная Информация'
        verbose_name_plural = 'Личная Информация'
    def __str__(self):
        return self.user.username


class Group(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)  # Отношение "многие ко многим" с моделью User

    def __str__(self):
        return self.name



class Add_Product(models.Model):
    name = models.TextField()
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


# class Activities(models.Model):
#     name = models.TextField()
#     calories_in = models.TextField()
#     time = models.TextField()

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

