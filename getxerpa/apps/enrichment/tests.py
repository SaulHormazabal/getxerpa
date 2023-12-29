from django.test import TestCase

from getxerpa.apps.enrichment.models import CategoryType, Category, Merchant, Keyword
from getxerpa.apps.transactions.models import Transaction


class EnrichmentTransactionModelTest(TestCase):
    def setUp(self):

        self.category_type = CategoryType.objects.create(name='expense')

        self.category_cargs = Category.objects.create(
            name='Automóvil & Transporte',
            type=self.category_type,
        )
        self.merchant_uber = Merchant.objects.create(
            name='Uber',
            category=self.category_cargs,
        )
        self.keyword_uber = Keyword.objects.create(
            name='uber',
            merchant=self.merchant_uber,
            weight=1,
        )

        self.category_restaurant = Category.objects.create(
            name='Restaurantes',
            type=self.category_type,
        )
        self.merchant_ubereats = Merchant.objects.create(
            name='Uber Eats',
            category=self.category_restaurant,
        )
        self.keyword_ubereats = Keyword.objects.create(
            name='uber eats',
            merchant=self.merchant_ubereats,
            weight=2,
        )

    def test_weight(self):
        transaction = Transaction.objects.create(
            description='UBER EATS',
            amount=100.0,
            date='2019-01-01',
        )

        self.assertEqual(transaction.enrichment.merchant_id, self.merchant_ubereats.id)
        self.assertEqual(transaction.enrichment.category_id, self.category_restaurant.id)

    def test_enrichment_null(self):
        transaction = Transaction.objects.create(
            description='indescifrable',
            amount=100.0,
            date='2019-01-01',
        )

        self.assertEqual(transaction.enrichment.merchant_id, None)
        self.assertEqual(transaction.enrichment.category_id, None)

    def test_category_without_merchant(self):
        Keyword.objects.create(
            name='pizza',
            category=self.category_restaurant,
            weight=2,
        )

        transaction = Transaction.objects.create(
            description='DOMINO PIZZA',
            amount=100.0,
            date='2019-01-01',
        )

        self.assertEqual(transaction.enrichment.merchant_id, None)
        self.assertEqual(transaction.enrichment.category_id, self.category_restaurant.id)
