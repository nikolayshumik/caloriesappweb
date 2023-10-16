from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .forms import UserRegistrationForm, PersonalInformForm, AddProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Add_Product
from .models import Breakfast_Products, Lunch_Products, Dinner_Products, Snack_Products
from django.db.models import Sum

from django.contrib.auth.decorators import login_required  # add this to your imports
# Create your views here.LoginForm,
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            # Выполнение входа пользователя после успешной регистрации
            login(request, new_user)

            return redirect('home')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def person_info(request):
    if request.method == 'POST':
        form = PersonalInformForm(request.POST)
        if form.is_valid():
            personal_info = form.save(commit=False)
            personal_info.user = request.user
            personal_info.save()
            # return redirect('/success_url/')
    else:
        form = PersonalInformForm()

    return render(request, 'register_done.html', {'form': form})


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
            return redirect('/')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
            return redirect('login')
    else:
        return render(request, 'login.html')


def calories_and_bjy(request):

    bcalories_in = Breakfast_Products.objects.aggregate(Sum('product__calories_in'))['product__calories_in__sum'] or 0
    bproteins = Breakfast_Products.objects.aggregate(Sum('product__proteins'))['product__proteins__sum'] or 0
    bfats = Breakfast_Products.objects.aggregate(Sum('product__fats'))['product__fats__sum'] or 0
    bcarbohydrates = Breakfast_Products.objects.aggregate(Sum('product__carbohydrates'))['product__carbohydrates__sum'] or 0

    calories_in = Lunch_Products.objects.aggregate(Sum('product__calories_in'))['product__calories_in__sum'] or 0
    proteins = Lunch_Products.objects.aggregate(Sum('product__proteins'))['product__proteins__sum'] or 0
    fats = Lunch_Products.objects.aggregate(Sum('product__fats'))['product__fats__sum'] or 0
    carbohydrates = Lunch_Products.objects.aggregate(Sum('product__carbohydrates'))['product__carbohydrates__sum'] or 0

    dcalories_in = Dinner_Products.objects.aggregate(Sum('product__calories_in'))['product__calories_in__sum'] or 0
    dproteins = Dinner_Products.objects.aggregate(Sum('product__proteins'))['product__proteins__sum'] or 0
    dfats = Dinner_Products.objects.aggregate(Sum('product__fats'))['product__fats__sum'] or 0
    dcarbohydrates = Dinner_Products.objects.aggregate(Sum('product__carbohydrates'))['product__carbohydrates__sum'] or 0

    scalories_in = Snack_Products.objects.aggregate(Sum('product__calories_in'))['product__calories_in__sum'] or 0
    sproteins = Snack_Products.objects.aggregate(Sum('product__proteins'))['product__proteins__sum'] or 0
    sfats = Snack_Products.objects.aggregate(Sum('product__fats'))['product__fats__sum'] or 0
    scarbohydrates = Snack_Products.objects.aggregate(Sum('product__carbohydrates'))['product__carbohydrates__sum'] or 0

    total_calories = bcalories_in + calories_in + dcalories_in + scalories_in
    total_proteins = bproteins + proteins + dproteins + sproteins
    total_carbohydrates = bcarbohydrates + carbohydrates + dcarbohydrates + scarbohydrates
    total_fats = bfats + fats + dfats + sfats

    breakfast_products = Breakfast_Products.objects.all()
    bproducts = [bp.product for bp in breakfast_products]

    lunch_products = Lunch_Products.objects.all()
    lproducts = [bp.product for bp in lunch_products]

    dinner_products = Dinner_Products.objects.all()
    dproducts = [bp.product for bp in dinner_products]

    snack_products = Snack_Products.objects.all()
    sproducts = [bp.product for bp in snack_products]

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
    return render(request, 'activities.html')
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
    product = Add_Product.objects.get(id=product_id)

    # Получите текущего пользователя с помощью `request.user` и создайте новую запись Breakfast_Products
    user = request.user
    Breakfast_Products.objects.create(product=product, user=user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_lunch_view(request):
    product_id = request.POST.get('product_id')
    product = Add_Product.objects.get(id=product_id)

    # Создайте новую запись Breakfast_Products
    Lunch_Products.objects.create(product=product)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_dinner_view(request):
    product_id = request.POST.get('product_id')
    product = Add_Product.objects.get(id=product_id)

    # Создайте новую запись Breakfast_Products
    Dinner_Products.objects.create(product=product)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_snack_view(request):
    product_id = request.POST.get('product_id')
    product = Add_Product.objects.get(id=product_id)

    # Создайте новую запись Breakfast_Products
    Snack_Products.objects.create(product=product)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
