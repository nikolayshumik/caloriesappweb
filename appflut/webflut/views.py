import os
import matplotlib
import calendar

import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
from babel.dates import format_datetime
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.utils.timezone import make_aware
from django.http import HttpResponseRedirect

from .forms import DateForm
from .forms import UserRegistrationForm, PersonalInformForm, AddProductForm, Step1Form, Step3Form

from .models import Add_Product, Ttime_Test, Breakfast_Products, Lunch_Products, Dinner_Products, Snack_Products
from .models import Activity, Personal_Inform, Activities_Add, Group

from django.views.generic import TemplateView

matplotlib.use('Agg')  # Использование фонового режима для Matplotlib


# Create your views here.LoginForm,
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data.get('user_type')

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            if user_type == 'trainer':
                # Дополнительная логика для регистрации тренера
                pass
            else:
                # Дополнительная логика для регистрации пользователя
                pass
            login(request, user)
            return redirect('step1')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def step1_view(request):
    if request.method == 'POST':
        form = Step1Form(request.POST)
        if form.is_valid():
            # Retrieve the existing Personal_Inform object for the current user
            try:
                personal_info = Personal_Inform.objects.get(user=request.user)
            except Personal_Inform.DoesNotExist:
                personal_info = Personal_Inform(user=request.user)

            # Update the fields with the entered values
            personal_info.first_name = form.cleaned_data['first_name']
            personal_info.last_name = form.cleaned_data['last_name']
            personal_info.date_of_birth = form.cleaned_data['date_of_birth']

            personal_info.save()

            return redirect('step2')
    else:
        form = Step1Form()

    context = {'form': form}
    return render(request, 'info1.html', context)


def step2_view(request):
    personal_inform = get_object_or_404(Personal_Inform, user=request.user)

    if request.method == 'POST':
        sex = request.POST.get('sex')
        if sex in ('M', 'F'):
            personal_inform.sex = sex
            personal_inform.save()
            return redirect('step3')

    context = {'personal_inform': personal_inform}
    return render(request, 'info2.html', context)


def step3_view(request):
    if request.method == 'POST':
        form = Step3Form(request.POST)
        if form.is_valid():
            # Retrieve the existing Personal_Inform object for the current user
            try:
                personal_info = Personal_Inform.objects.get(user=request.user)
            except Personal_Inform.DoesNotExist:
                personal_info = Personal_Inform(user=request.user)

            # Update the fields with the entered values
            personal_info.height = form.cleaned_data['height']
            personal_info.weight = form.cleaned_data['weight']

            personal_info.save()

            return redirect('step4')
    else:
        form = Step3Form()

    context = {'form': form}
    return render(request, 'info3.html', context)

def step4_view(request):
    personal_inform = get_object_or_404(Personal_Inform, user=request.user)

    if request.method == 'POST':
        active = request.POST.get('active')
        if active in ('L', 'M'):
            personal_inform.active = active
            personal_inform.save()
            return redirect('step5')

    context = {'personal_inform': personal_inform}
    return render(request, 'info4.html', context)

def step5_view(request):
    personal_inform = get_object_or_404(Personal_Inform, user=request.user)

    if request.method == 'POST':
        goals = request.POST.get('goals')
        if goals in ('L', 'M', 'F'):
            personal_inform.goals = goals
            personal_inform.save()
            return redirect('calories_and_bjy')

    context = {'personal_inform': personal_inform}
    return render(request, 'info5.html', context)
@login_required
def person_info(request):
    if Personal_Inform.objects.filter(user=request.user).exists():
        return redirect('edit_person_info')  # Redirect to a different page indicating that the information is already filled

    if request.method == 'POST':
        form = PersonalInformForm(request.POST)
        if form.is_valid():
            personal_info = form.save(commit=False)
            personal_info.user = request.user
            personal_info.save()
            return redirect('home')  # Redirect to the successful registration page
    else:
        form = PersonalInformForm()

    return render(request, 'register_done.html', {'form': form})

def edit_person_info(request):
    personal_info = Personal_Inform.objects.get(user=request.user)
    if request.method == 'POST':
        form = PersonalInformForm(request.POST, instance=personal_info)
        if form.is_valid():
            form.save()
            return redirect('edit_person_info')  # Redirect to the successful registration page
    else:
        form = PersonalInformForm(instance=personal_info)
    return render(request, 'edit_person_info.html', {'form': form, 'personal_info': personal_info})
def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('calories_and_bjy')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
            return redirect('login')
    else:
        return render(request, 'login.html')



@login_required
def calories_and_bjy(request):
    if 'date' in request.GET:
        selected_date = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()

    if 'move' in request.GET:
        if request.GET['move'] == 'next':
            selected_date += timedelta(days=1)
        elif request.GET['move'] == 'prev':
            selected_date -= timedelta(days=1)

    form = DateForm(initial={"date": selected_date.strftime('%Y-%m-%d')})
    formatted_date = format_datetime(selected_date, format='EEEE, d MMMM ', locale='ru')
    formatted_date = formatted_date.capitalize()

    request.session['selected_date'] = selected_date.strftime('%Y-%m-%d')

    user = request.user

    # Filter your queryset by user for each category
    breakfast_products = Breakfast_Products.objects.filter(user=user, date__date=selected_date)
    bproducts = [{
        'product': bp.product,
        'weight': bp.weight,
        'calories': bp.calories,
        'proteins': bp.proteins,
        'fats': bp.fats,
        'carbohydrates': bp.carbohydrates
    } for bp in breakfast_products]

    lunch_products = Lunch_Products.objects.filter(user=user, date__date=selected_date)
    lproducts = [{
        'product': bp.product,
        'weight': bp.weight,
        'calories': bp.calories,
        'proteins': bp.proteins,
        'fats': bp.fats,
        'carbohydrates': bp.carbohydrates
    } for bp in lunch_products]

    dinner_products = Dinner_Products.objects.filter(user=user, date__date=selected_date)
    dproducts = [{
        'product': bp.product,
        'weight': bp.weight,
        'calories': bp.calories,
        'proteins': bp.proteins,
        'fats': bp.fats,
        'carbohydrates': bp.carbohydrates
    } for bp in dinner_products]

    snack_products = Snack_Products.objects.filter(user=user, date__date=selected_date)
    sproducts = [{
        'product': bp.product,
        'weight': bp.weight,
        'calories': bp.calories,
        'proteins': bp.proteins,
        'fats': bp.fats,
        'carbohydrates': bp.carbohydrates
    } for bp in snack_products]

    # activity_prod = Activities_Add.objects.filter(user=user, date__date=selected_date)
    # activity = activity_prod

    user = request.user
    personal_info = Personal_Inform.objects.get(user=user)  # получить личную информацию пользователя
    weight = float(personal_info.weight)  # получить вес пользователя и преобразовать в float
    activity_prod = Activities_Add.objects.filter(user=user, date__date=selected_date)

    acttotal_calories = 0  # общее количество сожженных калорий
    activities_and_calories = []

    for activity in activity_prod:
        time = activity.time/60
        burned_calories = round(activity.product.met * weight * time, 1)
        acttotal_calories += round(burned_calories, 1)  # добавить к общему количеству
        activities_and_calories.append((activity, burned_calories))

    inf = Personal_Inform.objects.get(user=user)
    if inf.sex=='M':
        height2 = inf.height
        weight2 = inf.weight
        date_of_birth2 = inf.date_of_birth
        male = round(66.4730 + (5.0033 * height2) + (13.7516 * weight2) - (6.7550 * date_of_birth2), 1)
    else:
        height2 = inf.height
        weight2 = inf.weight
        date_of_birth2 = inf.date_of_birth
        male = round(655.0955 + (1.8496 * height2) + (9.5634 * weight2) - (4.6756 * date_of_birth2), 1)

    bcalories_in = breakfast_products.aggregate(Sum('calories'))['calories__sum'] or 0
    bproteins = breakfast_products.aggregate(Sum('proteins'))['proteins__sum'] or 0
    bfats = breakfast_products.aggregate(Sum('fats'))['fats__sum'] or 0
    bcarbohydrates = breakfast_products.aggregate(Sum('carbohydrates'))['carbohydrates__sum'] or 0

    calories_in = lunch_products.aggregate(Sum('calories'))['calories__sum'] or 0
    proteins = lunch_products.aggregate(Sum('proteins'))['proteins__sum'] or 0
    fats = lunch_products.aggregate(Sum('fats'))['fats__sum'] or 0
    carbohydrates = lunch_products.aggregate(Sum('carbohydrates'))['carbohydrates__sum'] or 0

    dcalories_in = dinner_products.aggregate(Sum('calories'))['calories__sum'] or 0
    dproteins = dinner_products.aggregate(Sum('proteins'))['proteins__sum'] or 0
    dfats = dinner_products.aggregate(Sum('fats'))['fats__sum'] or 0
    dcarbohydrates = dinner_products.aggregate(Sum('carbohydrates'))['carbohydrates__sum'] or 0

    scalories_in = snack_products.aggregate(Sum('calories'))['calories__sum'] or 0
    sproteins = snack_products.aggregate(Sum('proteins'))['proteins__sum'] or 0
    sfats = snack_products.aggregate(Sum('fats'))['fats__sum'] or 0
    scarbohydrates = snack_products.aggregate(Sum('carbohydrates'))['carbohydrates__sum'] or 0

    # acalories_in = activity_prod.aggregate(Sum('product__calories_in'))['product__calories_in__sum'] or 0

    bcalories_in = round(bcalories_in, 1)
    bproteins = round(bproteins, 1)
    bfats = round(bfats, 1)
    bcarbohydrates = round(bcarbohydrates, 1)

    calories_in = round(calories_in, 1)
    proteins = round(proteins, 1)
    fats = round(fats, 1)
    carbohydrates = round(carbohydrates, 1)

    dcalories_in = round(dcalories_in, 1)
    dproteins = round(dproteins, 1)
    dfats = round(dfats, 1)
    dcarbohydrates = round(dcarbohydrates, 1)

    scalories_in = round(scalories_in, 1)
    sproteins = round(sproteins, 1)
    sfats = round(sfats, 1)
    scarbohydrates = round(scarbohydrates, 1)

    total_calories = round((bcalories_in + calories_in + dcalories_in + scalories_in), 1)
    total_proteins = round((bproteins + proteins + dproteins + sproteins), 1)
    total_carbohydrates = round((bcarbohydrates + carbohydrates + dcarbohydrates + scarbohydrates), 1)
    total_fats = round((bfats + fats + dfats + sfats), 1)

    # total_calories_activities = 0
    # total_calories_activities += acalories_in

    water = WaterConsumption.objects.filter(user=request.user, date__date=selected_date).last()

    if water is not None:
        # Если запись найдена, получить значение amount
        amountwater = water.amount
    else:
        # Если запись не найдена, установить значение amount равным 0
        amountwater = 0


    context = {
        'bproducts': bproducts,
        'lproducts': lproducts,
        'dproducts': dproducts,
        'sproducts': sproducts,
        'bcalories_in': bcalories_in,
        'bproteins': bproteins,
        'bfats': bfats,
        'bcarbohydrates': bcarbohydrates,
        'calories_in': calories_in,
        'proteins': proteins,
        'fats': fats,
        'carbohydrates': carbohydrates,
        'dcalories_in': dcalories_in,
        'dproteins': dproteins,
        'dfats': dfats,
        'dcarbohydrates': dcarbohydrates,
        'scalories_in': scalories_in,
        'sproteins': sproteins,
        'sfats': sfats,
        'scarbohydrates': scarbohydrates,
        'total_calories': total_calories,
        'total_proteins': total_proteins,
        'total_carbohydrates': total_carbohydrates,
        'total_fats': total_fats,
        'activity_prod': activity_prod,
        'form': form,
        'formatted_date': formatted_date,
        'acttotal_calories': acttotal_calories,
        'activities_and_calories': activities_and_calories,
        'male': male,
        'amountwater': amountwater,

    }
    return render(request, 'calories_and_bjy.html', context)

@login_required
def profile(request):
    return render(request, 'profile.html')


def report(request):
    breakfast_products = Breakfast_Products.objects.all()
    products = [bp.product for bp in breakfast_products]
    return render(request, 'report.html', {'products': products})


def breakfast(request):
    search_query = request.GET.get('search')

    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'breakfast.html', {'form': form, 'search_query': search_query})

    else:
        form = AddProductForm()

    products = Add_Product.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'breakfast.html', {'form': form, 'products': products, 'search_query': search_query})
def lunch(request):
    search_query = request.GET.get('search')

    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'lunch.html', {'form': form, 'search_query': search_query})

    else:
        form = AddProductForm()

    products = Add_Product.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'lunch.html', {'form': form, 'products': products, 'search_query': search_query})
def dinner(request):
    search_query = request.GET.get('search')

    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'dinner.html', {'form': form, 'search_query': search_query})

    else:
        form = AddProductForm()

    products = Add_Product.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'dinner.html', {'form': form, 'products': products, 'search_query': search_query})
def snack(request):
    search_query = request.GET.get('search')

    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'snack.html', {'form': form, 'search_query': search_query})

    else:
        form = AddProductForm()

    products = Add_Product.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'snack.html', {'form': form, 'products': products, 'search_query': search_query})
def activities(request):
    search_query = request.GET.get('search')
    activity = Activity.objects.all()
    if search_query:
        activity = activity.filter(activity_type__icontains=search_query)
    return render(request, 'activities.html', {'activity': activity, 'search_query': search_query})
def eatingbase(request):
    search_query = request.GET.get('search', '')

    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'eatingbase.html', {'form': form, 'search_query': search_query})

    else:
        form = AddProductForm()

    products = Add_Product.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'eatingbase.html', {'form': form, 'products': products, 'search_query': search_query})


# def add_product(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         product = Add_Product.objects.get(pk=product_id)
#
#         breakfast_product = Breakfast_Products(product=product)
#         breakfast_product.save()
#
#     return redirect('breakfast') # Перенаправляет пользователя на страницу 'breakfast'


@login_required
def add_breakfast_view(request):
    product_id = request.POST.get('product_id')
    weight = request.POST.get('weight')
    selected_date_str = request.session.get('selected_date', None)

    if product_id and selected_date_str and weight:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            selected_datetime = datetime.combine(selected_date, datetime.now().time())
            selected_datetime_aware = make_aware(selected_datetime)
            product = Add_Product.objects.get(id=product_id)
            user = request.user

            calories = float(weight) * (float(product.calories_in) / 100)
            proteins = round(float(weight) * (float(product.proteins) / 100), 1)
            fats = round(float(weight) * (float(product.fats) / 100), 1)
            carbohydrates = round(float(weight) * (float(product.carbohydrates) / 100), 1)


            Breakfast_Products.objects.create(product=product, user=user, date=selected_datetime_aware, weight=weight,
                                              calories=calories, proteins=proteins, fats=fats, carbohydrates=carbohydrates)
        except Add_Product.DoesNotExist:
            pass
        except ValueError:
            pass
    else:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required
def add_lunch_view(request):
    product_id = request.POST.get('product_id')
    weight = request.POST.get('weight')
    selected_date_str = request.session.get('selected_date', None)

    if product_id and selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            selected_datetime = datetime.combine(selected_date, datetime.now().time())
            selected_datetime_aware = make_aware(selected_datetime)
            product = Add_Product.objects.get(id=product_id)
            user = request.user

            calories = float(weight) * (float(product.calories_in) / 100)
            proteins = round(float(weight) * (float(product.proteins) / 100), 1)
            fats = round(float(weight) * (float(product.fats) / 100), 1)
            carbohydrates = round(float(weight) * (float(product.carbohydrates) / 100), 1)

            Lunch_Products.objects.create(product=product, user=user, date=selected_datetime_aware, weight=weight,
                                              calories=calories, proteins=proteins, fats=fats, carbohydrates=carbohydrates)
        except Add_Product.DoesNotExist:
            pass
        except ValueError:
            pass
    else:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required
def add_dinner_view(request):
    product_id = request.POST.get('product_id')
    weight = request.POST.get('weight')
    selected_date_str = request.session.get('selected_date', None)

    if product_id and selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            selected_datetime = datetime.combine(selected_date, datetime.now().time())
            selected_datetime_aware = make_aware(selected_datetime)
            product = Add_Product.objects.get(id=product_id)
            user = request.user

            calories = float(weight) * (float(product.calories_in) / 100)
            proteins = round(float(weight) * (float(product.proteins) / 100), 1)
            fats = round(float(weight) * (float(product.fats) / 100), 1)
            carbohydrates = round(float(weight) * (float(product.carbohydrates) / 100), 1)

            Dinner_Products.objects.create(product=product, user=user, date=selected_datetime_aware, weight=weight,
                                              calories=calories, proteins=proteins, fats=fats, carbohydrates=carbohydrates)
        except Add_Product.DoesNotExist:
            pass
        except ValueError:
            pass
    else:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required
def add_snack_view(request):
    product_id = request.POST.get('product_id')
    weight = request.POST.get('weight')
    selected_date_str = request.session.get('selected_date', None)

    if product_id and selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            selected_datetime = datetime.combine(selected_date, datetime.now().time())
            selected_datetime_aware = make_aware(selected_datetime)
            product = Add_Product.objects.get(id=product_id)
            user = request.user

            calories = float(weight) * (float(product.calories_in) / 100)
            proteins = round(float(weight) * (float(product.proteins) / 100), 1)
            fats = round(float(weight) * (float(product.fats) / 100), 1)
            carbohydrates = round(float(weight) * (float(product.carbohydrates) / 100), 1)

            Snack_Products.objects.create(product=product, user=user, date=selected_datetime_aware, weight=weight,
                                              calories=calories, proteins=proteins, fats=fats, carbohydrates=carbohydrates)
        except Add_Product.DoesNotExist:
            pass
        except ValueError:
            pass
    else:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




@login_required
def add_activity_view(request):
    activity_id = request.POST.get('product_id')
    time = request.POST.get('time')
    selected_date_str = request.session.get('selected_date', None)

    if activity_id and time and selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            selected_datetime = datetime.combine(selected_date, datetime.now().time())
            selected_datetime_aware = make_aware(selected_datetime)
            activity = Activity.objects.get(id=activity_id)
            user = request.user
            Activities_Add.objects.create(product=activity, user=user, time=time, date=selected_datetime_aware)
        except Activity.DoesNotExist:
            pass
        except ValueError:
            pass
    else:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_list(request, product_id):
    if request.method == 'POST':
        meal_type = request.POST.get('meal_type', '')
        selected_date_str = request.session.get('selected_date', None)
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d") if selected_date_str else None

        try:
            if meal_type == 'breakfast':
                product = Breakfast_Products.objects.filter(product_id=product_id, user=request.user)
            elif meal_type == 'lunch':
                product = Lunch_Products.objects.filter(product_id=product_id, user=request.user)
            elif meal_type == 'dinner':
                product = Dinner_Products.objects.filter(product_id=product_id, user=request.user, date__date=selected_date)
            elif meal_type == 'snack':
                product = Snack_Products.objects.filter(product_id=product_id, user=request.user, date__date=selected_date)
            elif meal_type == 'activities':
                product = Activities_Add.objects.filter(product_id=product_id, user=request.user, date__date=selected_date)
            else:
                raise Http404("Invalid meal type.")

            product.delete()
            return redirect('calories_and_bjy')

        except (Breakfast_Products.DoesNotExist, Lunch_Products.DoesNotExist, Dinner_Products.DoesNotExist,
                Snack_Products.DoesNotExist, Activities_Add.DoesNotExist):
            return HttpResponse("Product not found")


def remove_from_list2(request, product_id):
    if request.method == 'POST':
        try:
            products = Breakfast_Products.objects.filter(product_id=product_id)
            products.delete()
            return redirect('calories_and_bjy')

        except Breakfast_Products.DoesNotExist:
            return HttpResponse("Product not found")


def delete_activity(request, id):
    activity_to_delete = Activities_Add.objects.get(pk=id)
    activity_to_delete.delete()

    return HttpResponseRedirect(reverse('calories_and_bjy'))




def date_view(request):
    if 'date' in request.GET:
        selected_date = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()

    if 'move' in request.GET:
        if request.GET['move'] == 'next':
            selected_date += timedelta(days=1)
        elif request.GET['move'] == 'prev':
            selected_date -= timedelta(days=1)

    form = DateForm(initial={"date": selected_date})
    models = Ttime_Test.objects.filter(date__date=selected_date)

    return render(request, 'date.html', {'form': form, 'models': models})


@login_required
def creategroup(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        group = Group.objects.create(name=group_name)
        return redirect('creategroup')

    groups = Group.objects.all()



    return render(request, 'creategroup.html', {'groups': groups,})

@login_required
def groupdetail(request, group_id):
    group = Group.objects.get(id=group_id)
    users = User.objects.all()
    return render(request, 'groupdetail.html', {'group': group, 'users': users})


def adduser(request, group_id):
    group = Group.objects.get(id=group_id)
    users = User.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
            group.users.add(user)  # Добавление пользователя к группе
            return redirect('groupdetail', group_id=group.id)
        except User.DoesNotExist:
            pass

    return render(request, 'groupdetail.html', {'group': group, 'users': users})

def removeuser(request, group_id):
    group = Group.objects.get(id=group_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        group.users.remove(user)  # Удаление пользователя из группы

    return redirect('groupdetail', group_id=group.id)

@login_required
def userinfo(request, user_id):
    if 'date' in request.GET:
        selected_date = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()

    if 'move' in request.GET:
        if request.GET['move'] == 'next':
            selected_date += timedelta(days=1)
        elif request.GET['move'] == 'prev':
            selected_date -= timedelta(days=1)
    form = DateForm(initial={"date": selected_date})

    selected_date += timedelta(days=1)
    request.session['selected_date'] = selected_date.strftime('%Y-%m-%d')
    user = User.objects.get(id=user_id)
    breakfast_products = Breakfast_Products.objects.filter(user=user, date__date=selected_date)
    bproducts = [{
        'product': bp.product,
        'weight': bp.weight
    } for bp in breakfast_products]

    lunch_products = Lunch_Products.objects.filter(user=user, date__date=selected_date)
    lproducts = [{
        'product': bp.product,
        'weight': bp.weight
    } for bp in lunch_products]

    dinner_products = Dinner_Products.objects.filter(user=user, date__date=selected_date)
    dproducts = [{
        'product': bp.product,
        'weight': bp.weight
    } for bp in dinner_products]

    snack_products = Snack_Products.objects.filter(user=user, date__date=selected_date)
    sproducts = [{
        'product': bp.product,
        'weight': bp.weight
    } for bp in snack_products]

    # user = request.user
    personal_info = Personal_Inform.objects.get(user=user)  # получить личную информацию пользователя
    weight = float(personal_info.weight)  # получить вес пользователя и преобразовать в float
    activity_prod = Activities_Add.objects.filter(user=user, date__date=selected_date)
    # Остальной код для получения данных пользователя

    acttotal_calories = 0  # общее количество сожженных калорий
    activities_and_calories = []

    for activity in activity_prod:
        burned_calories = round(activity.product.met * weight / activity.time, 1)
        acttotal_calories += burned_calories  # добавить к общему количеству
        activities_and_calories.append((activity, burned_calories))

    inf = Personal_Inform.objects.get(user=user)
    if inf.sex == 'M':
        height2 = inf.height
        weight2 = inf.weight
        date_of_birth2 = inf.date_of_birth
        male = round(66.4730 + (5.0033 * height2) + (13.7516 * weight2) - (6.7550 * date_of_birth2), 1)
    else:
        height2 = inf.height
        weight2 = inf.weight
        date_of_birth2 = inf.date_of_birth
        male = round(655.0955 + (1.8496 * height2) + (9.5634 * weight2) - (4.6756 * date_of_birth2), 1)

    bcalories_in = breakfast_products.aggregate(Sum('product__calories_in'))['product__calories_in__sum'] or 0
    bproteins = breakfast_products.aggregate(Sum('product__proteins'))['product__proteins__sum'] or 0
    bfats = breakfast_products.aggregate(Sum('product__fats'))['product__fats__sum'] or 0
    bcarbohydrates = breakfast_products.aggregate(Sum('product__carbohydrates'))['product__carbohydrates__sum'] or 0

    calories_in = lunch_products.aggregate(Sum('product__calories_in'))['product__calories_in__sum'] or 0
    proteins = lunch_products.aggregate(Sum('product__proteins'))['product__proteins__sum'] or 0
    fats = lunch_products.aggregate(Sum('product__fats'))['product__fats__sum'] or 0
    carbohydrates = lunch_products.aggregate(Sum('product__carbohydrates'))['product__carbohydrates__sum'] or 0

    dcalories_in = dinner_products.aggregate(Sum('product__calories_in'))['product__calories_in__sum'] or 0
    dproteins = dinner_products.aggregate(Sum('product__proteins'))['product__proteins__sum'] or 0
    dfats = dinner_products.aggregate(Sum('product__fats'))['product__fats__sum'] or 0
    dcarbohydrates = dinner_products.aggregate(Sum('product__carbohydrates'))['product__carbohydrates__sum'] or 0

    scalories_in = snack_products.aggregate(Sum('product__calories_in'))['product__calories_in__sum'] or 0
    sproteins = snack_products.aggregate(Sum('product__proteins'))['product__proteins__sum'] or 0
    sfats = snack_products.aggregate(Sum('product__fats'))['product__fats__sum'] or 0
    scarbohydrates = snack_products.aggregate(Sum('product__carbohydrates'))['product__carbohydrates__sum'] or 0

    # acalories_in = activity_prod.aggregate(Sum('product__calories_in'))['product__calories_in__sum'] or 0

    total_calories = bcalories_in + calories_in + dcalories_in + scalories_in
    total_proteins = bproteins + proteins + dproteins + sproteins
    total_carbohydrates = bcarbohydrates + carbohydrates + dcarbohydrates + scarbohydrates
    total_fats = bfats + fats + dfats + sfats

    # total_calories_activities = 0
    # total_calories_activities += acalories_in
    context = {
        'user': user,
        'form': form,
        'bproducts': bproducts,
        'lproducts': lproducts,
        'dproducts': dproducts,
        'sproducts': sproducts,
        'bcalories_in': bcalories_in,
        'bproteins': bproteins,
        'bfats': bfats,
        'bcarbohydrates': bcarbohydrates,
        'calories_in': calories_in,
        'proteins': proteins,
        'fats': fats,
        'carbohydrates': carbohydrates,
        'dcalories_in': dcalories_in,
        'dproteins': dproteins,
        'dfats': dfats,
        'dcarbohydrates': dcarbohydrates,
        'scalories_in': scalories_in,
        'sproteins': sproteins,
        'sfats': sfats,
        'scarbohydrates': scarbohydrates,
        'total_calories': total_calories,
        'total_proteins': total_proteins,
        'total_carbohydrates': total_carbohydrates,
        'total_fats': total_fats,
        'activity_prod': activity_prod,
        'acttotal_calories': acttotal_calories,
        'activities_and_calories': activities_and_calories,
        'male': male,
        'weight': weight,

    }

    return render(request, 'userinfo.html', context)








@login_required
def display_chart(request):
    user = request.user
    name = user.username
    week_start = datetime.now().date() - timedelta(days=6)
    user_dir = os.path.join('webflut', 'static', 'phototest', user.username)  # Создаем путь к папке пользователя

    # Проверяем, существует ли папка пользователя, и если нет, создаем ее
    image_dir = os.path.join(settings.BASE_DIR, user_dir)
    os.makedirs(image_dir, exist_ok=True)

    # Первая диаграмма - потраченные калории
    breakfast_products = Breakfast_Products.objects.filter(user=user, date__date__range=[week_start, date.today()])
    lunch_products = Lunch_Products.objects.filter(user=user, date__date__range=[week_start, date.today()])
    dinner_products = Dinner_Products.objects.filter(user=user, date__date__range=[week_start, date.today()])
    snack_products = Snack_Products.objects.filter(user=user, date__date__range=[week_start, date.today()])
    calories_by_day = {}
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        total_calories = (
                (breakfast_products.filter(date__date=current_date).aggregate(Sum('calories'))[
                     'calories__sum'] or 0)
                + (lunch_products.filter(date__date=current_date).aggregate(Sum('calories'))[
                       'calories__sum'] or 0)
                + (dinner_products.filter(date__date=current_date).aggregate(Sum('calories'))[
                       'calories__sum'] or 0)
                + (snack_products.filter(date__date=current_date).aggregate(Sum('calories'))[
                       'calories__sum'] or 0)
        )
        calories_by_day[current_date] = total_calories
    days = [calendar.day_name[d.weekday()] for d in calories_by_day.keys()]
    calories = list(calories_by_day.values())

    # Создание первой диаграммы
    plt.figure(figsize=(10, 6))
    plt.plot(days, calories, marker='o')
    plt.xlabel('День недели')
    plt.ylabel('Всего потраченных калорий')
    plt.title('Потраченные калории за неделю')
    plt.xticks(rotation=45)
    plt.tight_layout()
    image_path_1 = os.path.join(image_dir, 'chart_1.png')
    plt.savefig(image_path_1)
    plt.close()

    # Вторая диаграмма - сожженные калории
    personal_info = Personal_Inform.objects.get(user=user)
    weight = float(personal_info.weight)
    activities = Activities_Add.objects.filter(user=user, date__date__range=[week_start, datetime.now().date()])
    calories_by_day = {}
    for activity in activities:
        day = activity.date.date()
        burned_calories = round(activity.product.met * weight / activity.time, 1)
        if day not in calories_by_day:
            calories_by_day[day] = 0
        calories_by_day[day] += max(burned_calories, 0)

    dates = [day.strftime('%Y-%m-%d') for day in (week_start + timedelta(days=i) for i in range(7))]
    calories = [calories_by_day.get(datetime.strptime(date, '%Y-%m-%d').date(), 0) for date in dates]

    # Создание второй диаграммы
    plt.figure(figsize=(10, 6))
    plt.plot(dates, calories, marker='o')
    plt.xlabel('Дата')
    plt.ylabel('Сожженные калории')
    plt.title('Сожженные калории за неделю')
    plt.xticks(rotation=45)
    plt.tight_layout()
    image_path_2 = os.path.join(image_dir, 'chart_2.png')
    plt.savefig(image_path_2)
    plt.close()

    context = {
        # 'image_path_1': os.path.join(user_dir, 'chart_1.png'),  # Передаем путь к картинкам в контексте
        # 'image_path_2': os.path.join(user_dir, 'chart_2.png'),
        'name': name,
    }
    return render(request, 'chart.html', context)


from .models import WaterConsumption


def add_water_consumption(request):
    selected_date_str = request.session.get('selected_date', None)

    if request.method == 'POST':
        amount = int(request.POST.get('amount'))

        # Преобразовать строку даты в объект datetime
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d')

        # Получить последнюю запись потребления воды пользователя для выбранной даты
        previous_consumption = WaterConsumption.objects.filter(user=request.user, date=selected_date).last()

        if previous_consumption:
            # Если запись найдена, добавить новое значение к предыдущему и обновить
            total_amount = previous_consumption.amount + amount
            previous_consumption.amount = total_amount
            previous_consumption.save()
        else:
            # Если запись не найдена, создать новую запись с указанными значениями
            WaterConsumption.objects.create(user=request.user, amount=amount, date=selected_date)

        return redirect('calories_and_bjy')  # Редирект на страницу профиля пользователя
    return render(request, 'calories_and_bjy.html')





# Create your views here.

class ServiceWorkerView(TemplateView):
    template_name = 'sw.js'
    content_type = 'application/javascript'
    name = 'sw.js'