from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Personal_Inform(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line
    sex = models.TextField()
    date_of_birth = models.TextField()
    weight = models.TextField()
    height = models.TextField()

    # YOUR GOALS
    goals = models.TextField()

    # YOUR LIFESTYLE
    active = models.TextField()



class Add_Product(models.Model):
    name = models.TextField()
    calories_in = models.TextField()
    proteins = models.TextField()
    fats = models.TextField()
    carbohydrates = models.TextField()

class Breakfast_Products(models.Model):
    product = models.ForeignKey(Add_Product, on_delete=models.CASCADE)