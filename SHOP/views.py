from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .models import Category, Type, Brand, Product, HashTag
from cart.forms import CartAddProductForm


def product_list(request, type=None, filter_slug=None):
    category = None
    ttype = None
    brand = None
    categories = Category.objects.all()
    types = Type.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(stock__gt=0)
    if type == 'category':
        category = get_object_or_404(Category, slug=filter_slug)
        products = products.filter(category=category)

    if type == 'type':
        ttype = get_object_or_404(Type, slug=filter_slug)
        products = products.filter(type=ttype)

    if type == 'brand':
        brand = get_object_or_404(Brand, slug=filter_slug)
        products = products.filter(brand=brand)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'type': ttype,
                   'brand': brand,
                   'categories': categories,
                   'types': types,
                   'brands': brands,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, stock__gt=0)
    cart_product_form = CartAddProductForm()
    products_tags = product.hash_tag.all()
    similar_products = Product.objects.filter(hash_tag__in=products_tags).exclude(id=product.id)
    similar_products = similar_products.annotate(same_tags=Count('hash_tag')).order_by('-same_tags')[:4]
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form, 'similar_products':similar_products})

