from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from pytils.translit import slugify

from shop.cart import Cart
from shop.forms import NewUserForm, ProductQuantityForm
from shop.models import Product, ViewCount, Category, Gender, Manufacturer


def index(request):
    """
    Отображение главной страницы
    """
    brands = Manufacturer.objects.all()
    new_goods = Product.objects.all().order_by('-date')[:8]
    return render(request,
                  'index.html',
                  {"brands": brands,
                   "new_goods": new_goods})


def product_detail(request, slug):
    """
    Детальный показ товара
    """
    product = get_object_or_404(Product, slug=slug)

    if not request.user.is_anonymous:
        # получаем или создаем запись о просмотре товара для данного пользователя
        ViewCount.objects.get_or_create(product=product, username=request.user)

    return render(request, 'products/product_detail.html', {'product': product})


def products_list(request, slug=None):
    """
    Отображение списка всех товаров или по категориям
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)
    return render(request,
                  'products/product_list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'title': None})


def new_products_list(request):
    """
    Отображение списка всех новых товаров
    """
    new_goods = Product.objects.all().order_by('-date')
    return render(request,
                  'products/product_list.html',
                  {'category': None,
                   'categories': None,
                   'products': new_goods,
                   'title': 'Новинки'})


def gender_products_list(request, slug=None):
    """
    Отображение списка всех товаров по полу
    """
    gender_name = None
    products = Product.objects.all()
    if slug:
        gender = get_object_or_404(Gender, slug=slug)
        products = products.filter(gender=gender)
        gender_name = gender.name + " одежда"
    return render(request,
                  'products/product_list.html',
                  {'category': None,
                   'categories': None,
                   'products': products,
                   'title': gender_name})


def brands_list(request):
    """
    Отображение списка всех брендов
    """
    brands = Manufacturer.objects.all()
    return render(request,
                  'products/brand_list.html',
                  {'brands': brands})


def brand_products_list(request, slug=None):
    """
    Отображение списка всех товаров по бренду
    """
    brand_name = None
    products = Product.objects.all()
    if slug:
        brand = get_object_or_404(Manufacturer, slug=slug)
        products = products.filter(manufacturer=brand)
        brand_name = brand.name
    return render(request,
                  'products/product_list.html',
                  {'category': None,
                   'categories': None,
                   'products': products,
                   'title': brand_name})


def register(request):
    """
    Отображение регистрации
    """
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Успешная регистрация!")
            return redirect('home')
        messages.error(request, "Неудачная попытка регистрации. Неправильная информация")

    form = NewUserForm()
    return render(request, 'registration/register.html', {'register_form': form})


def profile(request):
    """
    Отображение профиля
    """
    return render(request, 'registration/profile.html')


def search(request):
    """Отображение списка товаров по запросу"""
    query = request.GET.get("query", 'Пустой запрос').strip()  # strip() убирает пробелы в начале и в конце
    slug_query = slugify(query)  # конвертируем в ссылку, так как sqlite не умеет работать с кириллицей
    products = Product.objects.all().filter(Q(name__icontains=slug_query) |
                                            Q(slug__icontains=slug_query) |
                                            Q(manufacturer__name__icontains=slug_query) |
                                            Q(category__slug__icontains=slug_query))
    return render(request,
                  'products/product_list.html',
                  {'products': products,
                   'title': f'Поиск ({query})'})


def add_to_cart(request, product_id, quantity=1, update_quantity=False):
    """
    Ссылка на добавление товара в корзину или его обновление
    """
    if request.method == "POST":
        quantity = int(ProductQuantityForm(request.POST)['quantity'].value())
        update_quantity = True
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, quantity=quantity, update_quantity=update_quantity)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # редирект на эту же страницу


def remove_from_cart(request, product_id):
    """
    Ссылка на удаление товара из корзины
    """
    Cart(request).remove(product_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # редирект на эту же страницу


def clear_cart(request):
    """
    Ссылка на очистку корзины товаров
    """
    Cart(request).clear()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # редирект на эту же страницу


def cart_detail(request):
    """
    Отображение списка товаров корзины
    """
    cart = Cart(request)
    for item in cart:
        item['quantity_form'] = ProductQuantityForm(initial={'quantity': item['quantity']})
    return render(request, 'cart/cart_detail.html',
                  {'cart': cart})


def order_processed(request):
    """Отображение сформированного заказа"""
    cart = Cart(request)
    if not cart:
        # если корзина пуста, то оформления заказа не будет
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # редирект на эту же страницу
    total_price = cart.total_price()
    ordered_items = [item for item in cart]  # формируем список купленных товаров
    cart.clear()  # очищаем список корзины
    return render(request, 'cart/order_processed.html', {'total_price': total_price, 'ordered_items': ordered_items})
