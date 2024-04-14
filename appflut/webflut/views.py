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

from .models import Add_Product, Ttime_Test, Breakfast_Products, Lunch_Products, Dinner_Products, Snack_Products, \
    Activity_for_children, Activities_Add_Children
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
    personal_info = Personal_Inform.objects.get(user=user)  # получить личную информацию пользователя
    weight = float(personal_info.weight)  # получить вес пользователя и преобразовать в float
    activity_prod = Activities_Add.objects.filter(user=user, date__date=selected_date)
    activity_prod_child = Activities_Add_Children.objects.filter(user=user, date__date=selected_date)

    acttotal_calories = 0  # общее количество сожженных калорий
    acttotal_calories_child = 0  # общее количество сожженных калорий
    activities_and_calories = []
    activities_and_calories_child = []

    user = request.user
    date_of_birth = Personal_Inform.objects.get(user=user).date_of_birth
    today = datetime.now().date()
    user_age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    for activity in activity_prod:
        time = activity.time/60
        burned_calories = round(activity.product.met * weight * time, 1)
        acttotal_calories += round(burned_calories, 1)  # добавить к общему количеству
        activities_and_calories.append((activity, burned_calories))
    for activity_child in activity_prod_child:
        if user_age<18:
            if user_age >= 16 and user_age <= 18:
                calories_field = activity_child.product.code_16_18
            elif user_age >= 13 and user_age <= 15:
                calories_field = activity_child.product.code_13_15
            elif user_age >= 10 and user_age <= 12:
                calories_field = activity_child.product.code_10_12
            elif user_age >= 6 and user_age <= 9:
                calories_field = activity_child.product.code_6_9
            else:

                calories_field = activity_child.product.code_16_18
            time_child = activity_child.time/60
            burned_calories_child = round(float(calories_field) * weight * time_child, 1)
            acttotal_calories_child += round(burned_calories_child, 1)  # добавить к общему количеству
            activities_and_calories_child.append((activity_child, burned_calories_child))

    inf = Personal_Inform.objects.get(user=user)
    date_of_birth = inf.date_of_birth
    today = datetime.now().date()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    if inf.sex=='M':
        height2 = inf.height
        weight2 = inf.weight
        date_of_birth2 = inf.date_of_birth
        male = round(66.4730 + (5.0033 * height2) + (13.7516 * weight2) - (6.7550 * age), 1)
    else:
        height2 = inf.height
        weight2 = inf.weight
        date_of_birth2 = inf.date_of_birth
        male = round(655.0955 + (1.8496 * height2) + (9.5634 * weight2) - (4.6756 * age), 1)


    context = {
        'activity_prod': activity_prod,
        'activity_prod_child': activity_prod_child,
        'form': form,
        'formatted_date': formatted_date,
        'acttotal_calories': acttotal_calories,
        'acttotal_calories_child': acttotal_calories_child,
        'activities_and_calories': activities_and_calories,
        'activities_and_calories_child': activities_and_calories_child,
        'male': male,
        'user_age': user_age,

    }
    return render(request, 'calories_and_bjy.html', context)

@login_required
def profile(request):
    return render(request, 'profile.html')


def report(request):
    breakfast_products = Breakfast_Products.objects.all()
    products = [bp.product for bp in breakfast_products]
    return render(request, 'report.html', {'products': products})




from django.db.models import Q

from django.shortcuts import render
from django.db.models import Q
from .models import Activity

def activities(request):
    search_query = request.GET.get('search')
    category_filter = request.GET.get('category')

    if search_query:
        search_query = search_query.capitalize()

    activities = Activity.objects.all()

    if search_query:
        activities = activities.filter(
            Q(activity_type__icontains=search_query) | Q(activity_type__contains=search_query)
        )

    categories = activities.values_list('category', flat=True).distinct()

    if category_filter:
        activities = activities.filter(category=category_filter)

    return render(request, 'activities.html', {'activities': activities, 'categories': categories})

def category_list(request):

    user = Personal_Inform.objects.get(user=request.user)
  # получение возраста пользователя
    date_of_birth = user.date_of_birth
    today = datetime.now().date()
    user_age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    if user_age < 18:
        categories = Activity_for_children.objects.values('category').distinct()
    else:
        categories = Activity.objects.values('category').distinct()
    return render(request, 'category_list.html', {'categories': categories})

def category_items(request, category):
    search_query = request.GET.get('search')
    user = Personal_Inform.objects.get(user=request.user)
    date_of_birth = user.date_of_birth
    today = datetime.now().date()
    user_age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    if user_age < 18:
        activities = Activity_for_children.objects.filter(category=category)
        if search_query:
            activities = Activity_for_children.filter(
                Q(activity_type__icontains=search_query) | Q(activity_type__contains=search_query)
            )
    else:
        activities = Activity.objects.filter(category=category)
        if search_query:
            activities = activities.filter(
                Q(activity_type__icontains=search_query) | Q(activity_type__contains=search_query)
            )

    return render(request, 'category_detail.html', {'activities': activities, 'user_age': user_age})

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
        search_query = search_query.capitalize()
        products = products.filter(Q(activity_type__icontains=search_query) | Q(activity_type__contains=search_query))

    return render(request, 'eatingbase.html', {'form': form, 'products': products, 'search_query': search_query})

@login_required
def add_activity_view(request):
    activity_id = request.POST.get('activities_id')
    time = request.POST.get('time')
    selected_date_str = request.session.get('selected_date', None)

    if activity_id and time and selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            selected_datetime = datetime.combine(selected_date, datetime.now().time())
            selected_datetime_aware = make_aware(selected_datetime)
            user = request.user
            date_of_birth = Personal_Inform.objects.get(user=user).date_of_birth
            today = datetime.now().date()
            user_age = today.year - date_of_birth.year - (
                        (today.month, today.day) < (date_of_birth.month, date_of_birth.day))

            if user_age < 18:
                activity = Activity_for_children.objects.get(id=activity_id)
                user = request.user
                Activities_Add_Children.objects.create(product=activity, user=user, time=time, date=selected_datetime_aware)
            else:
                activity = Activity.objects.get(id=activity_id)
                user = request.user
                Activities_Add.objects.create(product=activity, user=user, time=time, date=selected_datetime_aware)

        except (Activity_for_children.DoesNotExist, Activity.DoesNotExist):
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

            if meal_type == 'activities':
                product = Activities_Add.objects.filter(product_id=product_id, user=request.user, date__date=selected_date)
            else:
                raise Http404("Invalid meal type.")

            product.delete()
            return redirect('calories_and_bjy')

        except (Activities_Add.DoesNotExist):
            return HttpResponse("Product not found")



def delete_activity(request, id):
    user = request.user
    date_of_birth = Personal_Inform.objects.get(user=user).date_of_birth

    today = datetime.now().date()
    user_age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    if user_age<18:
        activity_to_delete = Activities_Add_Children.objects.get(pk=id)
        activity_to_delete.delete()
    else:
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

from django.db.models import Count
@login_required
def creategroup(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        user = request.user  # Получить текущего пользователя

        group = Group.objects.create(name=group_name, creator=user)  # Создать группу с указанием создателя
        return redirect('creategroup')

    # Получите список групп с количеством пользователей в каждой группе
    groups_with_users_count = Group.objects.filter(creator=request.user).annotate(num_users=Count('users'))

    return render(request, 'creategroup.html', {'groups': groups_with_users_count})

@login_required
def deletegroup(request, group_id):
    group = Group.objects.get(id=group_id)
    # Проверяем, что пользователь является создателем группы
    if request.user == group.creator:
        group.delete()  # Удаляем группу
    return redirect('creategroup')
@login_required
def groupdetail(request, group_id):
    group = Group.objects.get(id=group_id)
    users = User.objects.all()
    pers_info = Personal_Inform.objects.all()


    query = request.GET.get('q')
    usersserch = User.objects.filter(username__icontains=query) if query else User.objects.none()
    pers_info_search = pers_info.filter(first_name__icontains=query) if query else Personal_Inform.objects.none()

    return render(request, 'groupdetail.html', {'group': group, 'users': users, 'usersserch': usersserch, 'pers_info_search': pers_info_search, 'pers_info': pers_info})


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
def userinfo(request, user_id: int):
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

    selected_date += timedelta(days=1)
    request.session['selected_date'] = selected_date.strftime('%Y-%m-%d')
    user = User.objects.get(id=user_id)

    # user = request.user
    personal_info = Personal_Inform.objects.get(user=user)  # получить личную информацию пользователя
    weight = float(personal_info.weight)  # получить вес пользователя и преобразовать в float
    activity_prod = Activities_Add.objects.filter(user=user, date__date=selected_date)
    activity_prod_child = Activities_Add_Children.objects.filter(user=user, date__date=selected_date)

    acttotal_calories = 0  # общее количество сожженных калорий
    acttotal_calories_child = 0  # общее количество сожженных калорий
    activities_and_calories = []
    activities_and_calories_child = []

    user = request.user
    date_of_birth = Personal_Inform.objects.get(user=user).date_of_birth
    today = datetime.now().date()
    user_age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    for activity in activity_prod:
        time = activity.time / 60
        burned_calories = round(activity.product.met * weight * time, 1)
        acttotal_calories += round(burned_calories, 1)  # добавить к общему количеству
        activities_and_calories.append((activity, burned_calories))
    for activity_child in activity_prod_child:
        if user_age < 18:
            if user_age >= 16 and user_age <= 18:
                calories_field = activity_child.product.code_16_18
            elif user_age >= 13 and user_age <= 15:
                calories_field = activity_child.product.code_13_15
            elif user_age >= 10 and user_age <= 12:
                calories_field = activity_child.product.code_10_12
            elif user_age >= 6 and user_age <= 9:
                calories_field = activity_child.product.code_6_9
            else:

                calories_field = activity_child.product.code_16_18
            time_child = activity_child.time / 60
            burned_calories_child = round(float(calories_field) * weight * time_child, 1)
            acttotal_calories_child += round(burned_calories_child, 1)  # добавить к общему количеству
            activities_and_calories_child.append((activity_child, burned_calories_child))

    inf = Personal_Inform.objects.get(user=user)
    if inf.sex == 'M':
        height2 = inf.height
        weight2 = inf.weight
        date_of_birth2 = inf.date_of_birth
        male = round(66.4730 + (5.0033 * height2) + (13.7516 * weight2) - (6.7550 * user_age), 1)
    else:
        height2 = inf.height
        weight2 = inf.weight
        date_of_birth2 = inf.date_of_birth
        male = round(655.0955 + (1.8496 * height2) + (9.5634 * weight2) - (4.6756 * user_age), 1)


    context = {
        'activity_prod': activity_prod,
        'activity_prod_child': activity_prod_child,
        'user': user,
        'form': form,
        'formatted_date': formatted_date,
        'acttotal_calories': acttotal_calories,
        'acttotal_calories_child': acttotal_calories_child,
        'activities_and_calories': activities_and_calories,
        'activities_and_calories_child': activities_and_calories_child,
        'male': male,
        'personal_info': personal_info,

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
    plt.ylabel('сожженные калории')
    plt.title('сожженные калории за неделю')
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