from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class HashTag(models.Model):
    hash_tag = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Хэш-тег'
        verbose_name_plural = 'Хэш-теги'

    def __str__(self):
        return self.hash_tag


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='category/%Y/%m/%d', blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_',
                       args=['category', self.slug])


class Type(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='type/%Y/%m/%d', blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_',
                       args=['type', self.slug])


class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='brand/%Y/%m/%d', blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_',
                       args=['brand', self.slug])


class Product(models.Model):
    hash_tag = models.ManyToManyField(HashTag, related_name='tags', db_index=True, blank=True, null=True )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_index=True)
    category = models.ManyToManyField(Category)
    type = models.ManyToManyField(Type)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    name = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    description = models.TextField(blank=True, db_index=True)
    composition = models.CharField(max_length=200, db_index=True, blank=True)
    stock = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name', 'created', 'updated', 'stock', 'price')
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


