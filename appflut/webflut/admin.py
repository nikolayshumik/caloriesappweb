from django.contrib import admin
from .models import Personal_Inform
from .models import Add_Product
from .models import Breakfast_Products
from .models import Lunch_Products
from .models import Dinner_Products
from .models import Snack_Products

from .models import Activities_Add
from .models import Ttime_Test
from .models import Activity
from .models import Group
from .models import UserProfile
from .models import Step1Model
from .models import Step3Model
from .models import WaterConsumption
from .models import Activity_for_children
from .models import Activities_Add_Children

from django.contrib import admin




class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')

admin.site.register(UserProfile, UserProfileAdmin)



admin.site.register(Personal_Inform)
admin.site.register(Add_Product)
admin.site.register(Breakfast_Products)
admin.site.register(Lunch_Products)
admin.site.register(Dinner_Products)
admin.site.register(Snack_Products)

admin.site.register(Activities_Add)
admin.site.register(Ttime_Test)
admin.site.register(Activity)
admin.site.register(Group)
admin.site.register(Step1Model)
admin.site.register(Step3Model)
admin.site.register(WaterConsumption)
admin.site.register(Activity_for_children)
admin.site.register(Activities_Add_Children)
