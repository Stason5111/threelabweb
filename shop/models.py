from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Manufacturer(models.Model):
    """Бренд одежды"""
    name = models.CharField(max_length=255, help_text="Введите имя бренда")
    image = models.ImageField(upload_to=f'brands/', null=True, blank=True, help_text="Вставьте изображение бренда")
    slug = models.SlugField(max_length=255, db_index=True, unique=True, help_text='Сокращение для ссылки')

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории для одежды"""
    name = models.CharField(max_length=255, help_text='Введите название категории во множественном числе')
    singular_name = models.CharField(max_length=255, help_text='Введите название категории в единственном числе')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, help_text='Сокращение для ссылки')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products_list_by_category', args=[self.slug])


class Color(models.Model):
    """
    Модель цветов для одежды
    """
    name = models.CharField(max_length=255, help_text='Введите название цвета')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name


class Gender(models.Model):
    """
    Модель пола одежды
    """
    name = models.CharField(max_length=255, help_text='Выберите название пола')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, help_text='Сокращение для ссылки')

    class Meta:
        verbose_name = 'Пол одежды'
        verbose_name_plural = 'Пола одежды'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товара"""
    name = models.CharField(max_length=255, db_index=True, help_text="Введите название товара")
    image = models.ImageField(upload_to=f'products/', null=True, blank=True, help_text="Вставьте изображение товара")
    slug = models.SlugField(max_length=255, db_index=True, help_text='Сокращение для ссылки')
    price = models.DecimalField(default=1.0, max_digits=10, decimal_places=2,
                                help_text="Введите цену товара")  # DECIMAL точнее FLOAT
    manufacturer = models.ForeignKey(Manufacturer, models.SET_NULL, null=True, blank=True, help_text="Выберите бренд")
    gender = models.ForeignKey(Gender, models.SET_NULL, null=True, blank=True, help_text="Введите пол")
    color = models.ForeignKey(Color, models.SET_NULL, null=True, blank=True, help_text="Выберите расцветку одежды")
    description = models.CharField(max_length=1000, default='', blank=True, help_text="Введите описание товара")
    category = models.ForeignKey(Category, models.CASCADE, help_text="Введите категорию товара")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [models.Index(fields=['id', 'slug']),]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def get_view_count(self):
        """Возвращает количество просмотров для товара"""
        return self.views.count()


class ViewCount(models.Model):
    """Модель просмотров для товара"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views')
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')

    class Meta:
        ordering = ('-viewed_on',)
        indexes = [models.Index(fields=['-viewed_on'])]
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'

    def __str__(self):
        return self.product.name