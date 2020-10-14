from django.db import models
from django.contrib.auth.models import User

from nutella_lovers import settings


class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    en_id = models.CharField(max_length=255, unique=True, null=True)

    def __str__(self):
        return self.name

class PurchaseStores(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    nutriscore = models.CharField(max_length=20, null=True)
    barcode = models.TextField(null=False)
    details = models.TextField(null=True)
    thumbnail = models.TextField(null=True)
    categories = models.ManyToManyField(
        Categories,
        verbose_name="product's categories"
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
    product_replacement = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name="used_substitute",
        verbose_name="substitute"
    )
