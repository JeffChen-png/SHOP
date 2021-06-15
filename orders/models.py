from django.core.validators import RegexValidator
from django.db import models
from SHOP.models import Product
from customers.models import Customer
from django.contrib.auth.models import User


class Order(models.Model):
    braintree_id = models.CharField(max_length=150, blank=True)
    customer = models.ForeignKey(Customer, related_name='owner', on_delete=models.CASCADE, )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name='Телефон')
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    PAYMENT_STATUS = (
        ('PUC', 'Наличными при получении'),
        ('CUC', 'Картой при получении'),
        ('C', 'Картой на сайте'),
    )

    payment = models.CharField(max_length=3, choices=PAYMENT_STATUS, default='In processing',
                              help_text='Status of payment')

    LOAN_STATUS = (
        ('In processing', 'В обработке'),
        ('Awaiting departure', 'Ожидает отправки'),
        ('Send', 'Отправлен'),
        ('Delivered', 'Доставлен'),
    )

    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='m',
                              help_text='Status of delivering')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity