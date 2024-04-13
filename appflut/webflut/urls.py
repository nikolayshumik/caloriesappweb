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
    path('activities/', views.activities, name='activities'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<str:category>/', views.category_items, name='category_items'),

    path('add_activity_view/', views.add_activity_view, name='add_activity_view'),
    path('remove_from_list/<int:product_id>/', views.remove_from_list, name='remove_from_list'),

    path('delete_activity/<int:id>/', views.delete_activity, name='delete_activity'),
    path('edit_person_info/', views.edit_person_info, name='edit_person_info'),
    path('creategroup', views.creategroup, name='creategroup'),
    path('groupdetail/<int:group_id>', views.groupdetail, name='groupdetail'),
    path('adduser/<int:group_id>', views.adduser, name='adduser'),
    path('removeuser/<int:group_id>', views.removeuser, name='removeuser'),
    path('userinfo/<int:user_id>', views.userinfo, name='userinfo'),
    # path('add_product', views.add_product, name='add_product'),
    path('step1/', views.step1_view, name='step1'),
    path('step2/', views.step2_view, name='step2'),
    path('step3/', views.step3_view, name='step3'),
    path('step4/', views.step4_view, name='step4'),
    path('step5/', views.step5_view, name='step5'),
    path('display_chart/', views.display_chart, name='display_chart'),
    path('add-water/', views.add_water_consumption, name='add_water_consumption'),

    path('deletegroup/<int:group_id>/', views.deletegroup, name='deletegroup'),
    path('sw.js', views.ServiceWorkerView.as_view(), name=views.ServiceWorkerView.name,)


]