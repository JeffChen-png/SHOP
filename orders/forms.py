from django import forms
from django.contrib.auth.models import User

from customers.models import Customer
from .models import Order


class OrderCreateForm(forms.ModelForm):
    # customer = forms.CharField(max_length=80)
    class Meta:
        model = Order
        exclude = ('customer', 'created', 'updated', 'status', )
        # widgets = {'customer': forms.HiddenInput,}

    # def __init__(self, *args, **kwargs):
    #     super(OrderCreateForm, self).__init__(*args, **kwargs)
    #     print(args)
    #     print(kwargs)
    #     # self.initial['customer'] =


    # def clean_customer(self):
    #     customer = self.cleaned_data['customer']
    #     return Customer.objects.get(user=User.objects.get(username=customer).id)

    # def save(self, user):
    #     order = super(OrderCreateForm, self)
    #     order.customer = user
    #     order.save()
    #     return order