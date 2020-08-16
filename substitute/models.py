from django.db import models
from django.contrib.auth.models import User

from nutella_lovers import settings


class Categories(models.Model):
    category_name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.category_name

class PurchaseStores(models.Model):
    store_name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.store_name

class Products(models.Model):
    product_name = models.CharField(max_length=255, unique=True, null=False)
    nutriscore = models.CharField(max_length=20, null=True)
    barcode = models.TextField(null=False)
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
        settings.AUTH_USER_MODEL,
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
