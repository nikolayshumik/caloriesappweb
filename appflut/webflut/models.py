from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
# Create your models here.
class Personal_Inform(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line
    sex = models.TextField()
    date_of_birth = models.DateField()
    weight = models.IntegerField()
    height = models.IntegerField()

    # YOUR GOALS
    goals = models.TextField()

    # YOUR LIFESTYLE
    active = models.TextField()
    class Meta:
        verbose_name = 'Личная Информация'
        verbose_name_plural = 'Личная Информация'
    def __str__(self):
        return self.user



class Add_Product(models.Model):
    name = models.TextField()
    calories_in = models.IntegerField()
    proteins = models.IntegerField()
    fats = models.IntegerField()
    carbohydrates = models.IntegerField()
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
    weight = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'Продукты Завтрака'
        verbose_name_plural = 'Продукты Завтрака'
    def __str__(self):
        return self.product.name

class Lunch_Products(models.Model):
    product = models.ForeignKey(Add_Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    date = models.DateTimeField(default=timezone.now)
    weight = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'Продукты Обеда'
        verbose_name_plural = 'Продукты Обеда'
    def __str__(self):
        return self.product.name

class Dinner_Products(models.Model):
     product = models.ForeignKey(Add_Product, on_delete=models.CASCADE)
     user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
     date = models.DateTimeField(default=timezone.now)
     weight = models.IntegerField(default=0)
     class Meta:
         verbose_name = 'Продукты Ужина'
         verbose_name_plural = 'Продукты Ужина'
     def __str__(self):
        return self.product.name




class Snack_Products(models.Model):
    product = models.ForeignKey(Add_Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    date = models.DateTimeField(default=timezone.now)
    weight = models.IntegerField(default=0)
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

