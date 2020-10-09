from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
from django.db.models import Count, Q

from .models import Products, Categories


def search_substitute(request):
    if request.method != 'GET':
        return

    search_input = request.GET['q'] # TODO: Virer le q

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
  