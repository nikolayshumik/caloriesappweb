from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .forms import UserRegistrationForm, PersonalInformForm, AddProductForm, Step1Form, Step2Form, Step3Form, Step4Form, StepTestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Add_Product, Ttime_Test
from .models import Breakfast_Products, Lunch_Products, Dinner_Products, Snack_Products, Activity, Personal_Inform, Activities_Add
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required  # add this to your imports
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
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
    if request.method == 'POST':
        form = Step2Form(request.POST)
        if form.is_valid():
            # Retrieve the existing Personal_Inform object for the current user
            try:
                personal_info = Personal_Inform.objects.get(user=request.user)
            except Personal_Inform.DoesNotExist:
                personal_info = Personal_Inform(user=request.user)

            # Update the fields with the entered values
            personal_info.sex = form.cleaned_data['sex']


            personal_info.save()

            return redirect('step3')
    else:
        form = Step2Form()

    context = {'form': form}
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
    if request.method == 'POST':
        form = Step4Form(request.POST)
        if form.is_valid():
            # Retrieve the existing Personal_Inform object for the current user
            try:
                personal_info = Personal_Inform.objects.get(user=request.user)
            except Personal_Inform.DoesNotExist:
                personal_info = Personal_Inform(user=request.user)

            # Update the fields with the entered values
            personal_info.goals = form.cleaned_data['goals']
            personal_info.active = form.cleaned_data['active']

            personal_info.save()

            return redirect('calories_and_bjy')
    else:
        form = StepTestForm()

    context = {'form': form}
    return render(request, 'info4.html', context)
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
            return redirect('home')  # Redirect to the successful registration page
    else:
        form = PersonalInformForm(instance=personal_info)
    return render(request, 'edit_person_info.html', {'form': form})
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
    form = DateForm(initial={"date": selected_date})

    selected_date += timedelta(days=1)
    request.session['selected_date'] = selected_date.strftime('%Y-%m-%d')

    user = request.user

    # Filter your queryset by user for each category
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

    # activity_prod = Activities_Add.objects.filter(user=user, date__date=selected_date)
    # activity = activity_prod

    user = request.user
    personal_info = Personal_Inform.objects.get(user=user)  # получить личную информацию пользователя
    weight = float(personal_info.weight)  # получить вес пользователя и преобразовать в float
    activity_prod = Activities_Add.objects.filter(user=user, date__date=selected_date)

    acttotal_calories = 0  # общее количество сожженных калорий
    activities_and_calories = []

    for activity in activity_prod:
        burned_calories = round(activity.product.met * weight / activity.time, 1)
        acttotal_calories += burned_calories  # добавить к общему количеству
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
        'acttotal_calories': acttotal_calories,
        'activities_and_calories': activities_and_calories,
        'male': male,

    }
    return render(request, 'calories_and_bjy.html', context)

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
    search_query = request.GET.get('search')

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
            Breakfast_Products.objects.create(product=product, user=user, date=selected_datetime_aware, weight=weight)
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
            Lunch_Products.objects.create(product=product, user=user, date=selected_datetime_aware, weight=weight)
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
            Dinner_Products.objects.create(product=product, user=user, date=selected_datetime_aware, weight=weight)
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
            Snack_Products.objects.create(product=product, user=user, date=selected_datetime_aware, weight=weight)
        except Add_Product.DoesNotExist:
            pass
        except ValueError:
            pass
    else:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

from django.utils.timezone import make_aware


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

# def remove_from_list(request, instance_id):
#     if request.method == 'POST':
#         meal_type = request.POST.get('meal_type','') # Получаем тип продукта для удаления из POST
#         if meal_type == 'breakfast':
#             product = get_object_or_404(Breakfast_Products, id=instance_id, user=request.user)
#         elif meal_type == 'lunch':
#             product = get_object_or_404(Lunch_Products, id=instance_id, user=request.user)
#         elif meal_type == 'dinner':
#             product = get_object_or_404(Dinner_Products, id=instance_id, user=request.user)
#         elif meal_type == 'snack':
#             product = get_object_or_404(Snack_Products, id=instance_id, user=request.user)
#         elif meal_type == 'activities':
#             product = get_object_or_404(Activities_Add, id=instance_id, user=request.user)
#         else:
#             raise Http404("Invalid meal type.")  # Или другой подход к обработке ошибок
#
#         product.delete()
#         return redirect('calories_and_bjy')

from datetime import datetime


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

from django.http import HttpResponseRedirect
from .models import Activities_Add
from django.urls import reverse
def delete_activity(request, id):
    activity_to_delete = Activities_Add.objects.get(pk=id)
    activity_to_delete.delete()

    return HttpResponseRedirect(reverse('calories_and_bjy'))



from django.shortcuts import render
from .forms import DateForm
from datetime import datetime, timedelta
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


from .models import Group
def creategroup(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        group = Group.objects.create(name=group_name)
        return redirect('creategroup')

    groups = Group.objects.all()



    return render(request, 'creategroup.html', {'groups': groups,})

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

    }

    return render(request, 'userinfo.html', context)






import matplotlib
matplotlib.use('Agg')  # Использование фонового режима для Matplotlib
import matplotlib.pyplot as plt
# import datetime


from django.conf import settings
import os
from datetime import datetime, timedelta, date

def display_calories_chart(request):
    user = request.user
    personal_info = Personal_Inform.objects.get(user=user)
    weight = float(personal_info.weight)

    week_start = datetime.now().date() - timedelta(days=6)
    activity_prod = Activities_Add.objects.filter(user=user, date__date__range=[week_start, date.today()])

    acttotal_calories = 0
    activities_and_calories = []

    for activity in activity_prod:
        burned_calories = round(activity.product.met * weight / activity.time, 1)
        acttotal_calories += burned_calories
        activities_and_calories.append((activity.date.date(), burned_calories))

    dates = [activity[0] for activity in activities_and_calories]
    calories = [activity[1] for activity in activities_and_calories]

    plt.plot(dates, calories, marker='o')
    plt.xlabel('Дата')
    plt.ylabel('Сожженные калории')
    plt.title('Сожженные калории за неделю')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Получите путь к текущему файлу
    current_path = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(current_path, 'static', 'phototest')
    os.makedirs(image_dir, exist_ok=True)

    image_path = os.path.join(image_dir, 'calories_chart.png')
    plt.savefig(image_path)  # Сохранить диаграмму как изображение
    plt.close()

    return render(request, 'chart.html', {'image_path': '/static/phototest/calories_chart.png'})


import calendar

def display(request):
    user = request.user
    week_start = datetime.now().date() - timedelta(days=6)

    # Retrieve consumed products for each meal type
    breakfast_products = Breakfast_Products.objects.filter(user=user, date__date__range=[week_start, date.today()])
    lunch_products = Lunch_Products.objects.filter(user=user, date__date__range=[week_start, date.today()])
    dinner_products = Dinner_Products.objects.filter(user=user, date__date__range=[week_start, date.today()])
    snack_products = Snack_Products.objects.filter(user=user, date__date__range=[week_start, date.today()])

    # Calculate calories sum for each day
    calories_by_day = {}
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        total_calories = (
                (breakfast_products.filter(date__date=current_date).aggregate(Sum('product__calories_in'))[
                     'product__calories_in__sum'] or 0)
                + (lunch_products.filter(date__date=current_date).aggregate(Sum('product__calories_in'))[
                       'product__calories_in__sum'] or 0)
                + (dinner_products.filter(date__date=current_date).aggregate(Sum('product__calories_in'))[
                       'product__calories_in__sum'] or 0)
                + (snack_products.filter(date__date=current_date).aggregate(Sum('product__calories_in'))[
                       'product__calories_in__sum'] or 0)
        )
        calories_by_day[current_date] = total_calories

    # Prepare chart data
    days = [calendar.day_name[d.weekday()] for d in calories_by_day.keys()]
    calories = list(calories_by_day.values())

    # Plot the chart
    plt.bar(days, calories)
    plt.xlabel('Day of the Week')
    plt.ylabel('Total Calories')
    plt.title('Total Consumed Calories by Day')
    plt.tight_layout()

    # Save the chart as an image
    current_path = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(current_path, 'static', 'phototest')
    os.makedirs(image_dir, exist_ok=True)

    image_path = os.path.join(image_dir, 'chart.png')
    plt.savefig(image_path)
    plt.close()

    context = {
        'image_path': '/static/phototest/chart.png',
    }
    return render(request, 'display.html', context)