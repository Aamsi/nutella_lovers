from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse

from .models import Products


def search_substitute(request):
    if request.method == 'GET':
        search_input = request.GET['q']

        products_found = Products.objects.annotate(
            search=SearchVector('name', 'details', 'categories__name')
        ).filter(search=search_input)

        categories_pk = []
        for product in products_found:
            for category_pk in product.categories.values_list('pk', flat=True):
                categories_pk.append(category_pk)

        categories_pk = sorted(set(categories_pk))

        # Pas trouve de moyen pour prendre directement les produits qui ont au moins X categories dans la liste
        products = Products.objects.filter(categories__in=categories_pk)
        products = sorted(
            set(products),
            key=lambda prod: prod.pk
        )

        effective_products = []
        for product in products:
            i = 0
            for cat in product.categories.values_list("pk", flat=True):
                if cat not in categories_pk:
                    continue
                i += 1
            if i >= 5:
                effective_products.append(product)

        return HttpResponse([product.name + "</br>" for product in effective_products])

        
        
        