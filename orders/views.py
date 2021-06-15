from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .tasks import order_created
from django.urls import reverse
from SHOP.models import Product
from customers.models import Customer
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


@login_required
def order_create(request):
    Customer.objects.get_or_create(user=request.user)
    cart = Cart(request)
    # form = OrderCreateForm({'customer': request.user.profile})
    if request.method == 'POST':
        form = OrderCreateForm(data=request.POST)
        if form.is_valid():
            # cd = form.cleaned_data
            order = form.save(commit=False)
            # Добавляем пользователя к созданному объекту.
            order.customer = request.user.profile
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
                count = Product.objects.get(id=item['product'].id).stock - item['quantity']
                Product.objects.filter(id=item['product'].id).update(stock=count)
            # Очищаем корзину.
            cart.clear()
            # Запуск асинхронной задачи.
            order_created.delay(order.id)
            # Сохранение заказа в сессии
            print(order.payment)
            if order.payment == 'C' or order.payment == 'CUC':
                request.session['order_id'] = order.id
                # Перенаправление на страницу оплаты.
                return redirect(reverse('payment:process'))
            elif order.payment == 'PUC':
            # messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            # return redirect('shop:product_list')
                return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})