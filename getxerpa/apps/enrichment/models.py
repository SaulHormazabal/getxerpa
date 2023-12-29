import uuid

from django.db import models
from rest_framework.fields import uuid
from django_pgviews import view as pg

from getxerpa.apps.transactions.models import Transaction


class CategoryType(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    type = models.ForeignKey(CategoryType, on_delete=models.CASCADE, related_name='categories')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Merchant(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    logo = models.URLField(null=True)

    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name='merchants')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Keyword(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='keywords')
    weight = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


ENRICHMENT_TRANSACTION_SQL = '''
    SELECT
        DISTINCT ON (t.id) t.id,
        t.description,

        m.id AS merchant_id,
        m.name AS merchant_name,

        c.id AS category_id,
        c.name AS category_name

    FROM
        transactions_transaction t
    LEFT JOIN
        enrichment_keyword k ON t.description ILIKE '%' || k.name || '%'
    LEFT JOIN
        enrichment_merchant m ON k.merchant_id = m.id
    LEFT JOIN
        enrichment_category c ON c.id = m.category_id
    ORDER BY
        t.id,
        k.weight DESC
    ;
'''


class EnrichmentTransaction(pg.View):

    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='enrichment')

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='enrichments')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='enrichments')
    keywords = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='enrichments')

    sql = ENRICHMENT_TRANSACTION_SQL

    class Meta:
        managed = False