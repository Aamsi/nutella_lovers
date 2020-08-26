from django.test import TestCase
from django.urls import reverse

from .models import Categories, PurchaseStores, Products


class SearchReplacementTest(TestCase):

    def setUp(self):
        category = Categories.objects.create(
            name="Epicerie",
            en_id="en:seeds"
        )
        store = PurchaseStores.objects.create(
            name="Carrefour"
        )
        product_0 = Products.objects.create(
            name="Riz long grain",
            nutriscore="b",
            barcode="5940356894303",
            details="Riz",
            purchase_store=store
        )
        product_1 = Products.objects.create(
            name="Riz allege",
            nutriscore="a",
            barcode="435643424325432",
            details="Riz allege",
            purchase_store=store
            )
        product_0.categories.add(category)
        product_1.categories.add(category)

    # def test_find_product_succeed(self):
    #     user_input = "Riz"
    #     response = self.client.get(reverse('search'), {
    #         "q": user_input
    #     })
    #     self.assertIn('Riz long grain', response.content.decode())


    # def test_find_product_failed(self):
        # user_input = "Jus"
        # response = self.client.get(reverse('search'), {
        #     "q": user_input
        # })
        # self.assertNotIn('Riz long grain', response.content.decode())

    def test_find_replacements_succeed(self):
        user_input = "Riz"
        response = self.client.get(reverse('search'), {
            "q": user_input
        })
        self.assertIn('Riz allege', response.content.decode())

    def test_find_replacements_failed(self):
        user_input = "Jus"
        response = self.client.get(reverse('search'), {
            "q": user_input
        })
        self.assertNotIn('Riz allege', response.content.decode())

