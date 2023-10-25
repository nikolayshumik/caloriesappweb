from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('person_info/', views.person_info, name='person_info'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('calories_and_bjy/', views.calories_and_bjy, name='calories_and_bjy'),
    path('profile/', views.profile, name='profile'),
    path('report/', views.report, name='report'),
    path('breakfast/', views.breakfast, name='breakfast'),
    path('lunch/', views.lunch, name='lunch'),
    path('dinner/', views.dinner, name='dinner'),
    path('snack/', views.snack, name='snack'),
    path('activities/', views.activities, name='activities'),
    path('eatingbase/', views.eatingbase, name='eatingbase'),
    path('add_breakfast/', views.add_breakfast_view, name='add_breakfast_view'),
    path('add_lunch/', views.add_lunch_view, name='add_lunch_view'),
    path('add_dinner/', views.add_dinner_view, name='add_dinner_view'),
    path('add_snack/', views.add_snack_view, name='add_snack_view'),
    path('add_activity_view/', views.add_activity_view, name='add_activity_view'),
    path('remove_from_list/<int:product_id>/', views.remove_from_list, name='remove_from_list'),
    path('delete_activity/<int:id>/', views.delete_activity, name='delete_activity'),
    path('edit_person_info/', views.edit_person_info, name='edit_person_info'),
    path('creategroup', views.creategroup, name='creategroup'),
    path('groupdetail/<int:group_id>', views.groupdetail, name='groupdetail'),
    path('adduser/<int:group_id>', views.adduser, name='adduser'),
    path('removeuser/<int:group_id>', views.removeuser, name='removeuser'),
    # path('add_product', views.add_product, name='add_product'),

]