from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    category_name = models.CharField(max_length=255, unique=True, null=False)

class PurchaseStores(models.Model):
    store_name = models.CharField(max_length=255, unique=True, null=False)

class Products(models.Model):
    product_name = models.CharField(max_length=255, unique=True, null=False)
    nutri_score = models.CharField(max_length=1, null=True)
    link = models.TextField(null=False)
    details = models.TextField(null=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        verbose_name="product's category"
    )
    purchase_store = models.ForeignKey(
        PurchaseStores,
        on_delete=models.CASCADE,
        verbose_name="purchase store"
    )

class Favorites(models.Model):
    fav_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favs',
        verbose_name="user's favorites substitutes"
    )
    product_replaced = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name="replaced",
        verbose_name="replaced product"
    )
    product_replacement = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name="used_substitute",
        verbose_name="substitute"
    )
