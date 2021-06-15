from django.urls import path
from . import views


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<str:type>/<slug:filter_slug>/', views.product_list, name='product_list_by_'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]