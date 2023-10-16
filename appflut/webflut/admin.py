from django.contrib import admin
from .models import Personal_Inform
from .models import Add_Product
from .models import Breakfast_Products
from .models import Lunch_Products
from .models import Dinner_Products
from .models import Snack_Products
# Register your models here.
admin.site.register(Personal_Inform)
admin.site.register(Add_Product)
admin.site.register(Breakfast_Products)
admin.site.register(Lunch_Products)
admin.site.register(Dinner_Products)
admin.site.register(Snack_Products)