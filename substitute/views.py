from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q

from .models import Products, Categories, Favorites, User

@login_required
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
    favs = []
    if request.user.is_authenticated:
        favs = request.user.favs.values_list('product_replacement__id', flat=True)
    return render(request, 'substitute/search_result.html', {
        'products': effective_products,
        'favs': favs
    })

@login_required
def my_favs(request):
    if request.method != 'GET':
        return
    favs = Favorites.objects.filter(fav_user=request.user)\
    .values_list('product_replacement', flat=True)
    fav_products = Products.objects.filter(id__in=favs)
    return render(request, 'substitute/favs.html', {
        'favs': fav_products
    })


@login_required
def save_substitute(request):
    if request.method != 'GET':
        return
    product_id = int(request.GET['product_id'])
    saved_prod = Products.objects.get(id=product_id)
    if not saved_prod:
        return JsonResponse({'success': False})
    Favorites.objects.get_or_create(
        fav_user=request.user,
        product_replacement=saved_prod
    )
    return JsonResponse({"success": True})

@login_required
def forget_substitute(request):
    if request.method != 'GET':
        return
    product_id = int(request.GET['product_id'])
    forgot_prod = Favorites.objects.get(
        fav_user=request.user,
        product_replacement=Products.objects.get(id=product_id)
    )
    if not forgot_prod:
        return JsonResponse({'success': False})
    forgot_prod.delete()
    return JsonResponse({'success': True})

