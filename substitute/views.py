from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q

from .models import Products, Categories, Favorites, User


def search_substitute(request):
    if request.method != 'GET':
        return

    search_input = request.GET['q']

    products_found = Categories.objects.annotate(
        search=SearchVector('products__name')
    ).filter(search=search_input)

    effective_products = Products.objects.annotate(
            common_category=Count("categories", filter=Q(categories__in=products_found)))\
            .filter(common_category__gt=5)\
            .order_by("nutriscore", "-common_category")[:20]
    return render(request, 'substitute/search_result.html', {
        'products': effective_products
    })

@login_required
def save_substitute(request):
    if request.method != 'GET':
        return
    product_id = int(request.GET['product_id'])
    print(product_id)
    saved_prod = Products.objects.get(id=product_id)
    Favorites.objects.get_or_create(
        fav_user=request.user,
        product_replacement=saved_prod
    )
    return JsonResponse({"success": True})