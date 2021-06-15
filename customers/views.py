from random import randint

from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # забираем IP адрес из запроса
        ip = get_client_ip(request)
        # получаем или создаём новую запись об IP, с которого вводится пароль, на предмет блокировки
        obj, created = TemporaryBanIp.objects.get_or_create(
            defaults={
                'ip_address': ip,
                'time_unblock': timezone.now()
            },
            ip_address=ip
        )

        if obj.status is True and obj.time_unblock > timezone.now():
            if obj.attempts == 3 or obj.attempts == 6:
                # то открываем страницу с сообщением о блокировки на 15 минут при 3 и 6 неудачных попытках входа
                return render(request, 'account/block_15_minutes.html')
            elif obj.attempts == 9:
                # или открываем страницу о блокировке на 24 часа, при 9 неудачных попытках входа
                return render(request, 'account/block_24_hours.html')
        elif obj.status is True and obj.time_unblock < timezone.now():
            # если IP заблокирован, но время разблокировки настало, то разблокируем IP
            obj.status = False
            obj.save()


        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    # gen_number = randint(10000, 99999)
                    # send_mail("2FA", "Your code: {}".format(gen_number), 'rrmedvedev@gmail.com', [user.email])
                    # return render(request, 'account/2AF_submite.html', {'form': DoubleAuth()})
                    gen_number = randint(100000, 999999)
                    send_mail("2FA", "Your code: {}".format(gen_number), 'rrmedvedev@gmail.com', [user.email])

                    if request.method == 'POST':
                        auth_form = DoubleAuth(request.POST)
                        if auth_form.is_valid():
                            cd = auth_form.cleaned_data
                            if cd['code'] == str(gen_number):
                                login(request, user)
                                messages.success(request, 'Authenticated successfully')
                                return redirect(reverse('shop:product_list'))
                            else:
                                messages.error(request, 'Login error')
                                return redirect(reverse('customers:login'))
                    else:
                        auth_form = DoubleAuth()
                    return render(request, 'account/2AF_submite.html', {'form': auth_form})
                else:
                    messages.error(request, 'Disabled account')
                    return redirect(reverse('customers:login'))
            else:
                # иначе считаем попытки и устанавливаем время разблокировки и статус блокировки
                obj.attempts += 1
                if obj.attempts == 3 or obj.attempts == 6:
                    obj.time_unblock = timezone.now() + timezone.timedelta(minutes=15)
                    obj.status = True
                elif obj.attempts == 9:
                    obj.time_unblock = timezone.now() + timezone.timedelta(1)
                    obj.status = True
                elif obj.attempts > 9:
                    obj.attempts = 1
                obj.save()
                messages.error(request, 'Invalid login')
                return redirect(reverse('customers:login'))
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в базе данных.
            new_user.save()
            # Создание профиля пользователя.
            Customer.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def profilepage(request):
    customer = request.user
    return render(request, 'account/profile.html', {'customer':customer})


@login_required
def edit(request):
    Customer.objects.get_or_create(user_id=request.user.id)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            # aes накинуть
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(reverse('customers:profile'))
        else:
            messages.error(request, 'Error updating your profile')
            return redirect(reverse('customers:edit'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})