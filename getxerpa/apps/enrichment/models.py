import uuid

from django.db import models
from django_pgviews import view as pg

from getxerpa.apps.transactions.models import Transaction


class Category(models.Model):

    class Types(models.IntegerChoices):
        EXPENSE = -1, 'expense'
        INCOME = 1, 'income'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    type = models.SmallIntegerField(default=Types.EXPENSE, choices=Types.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Merchant(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    logo = models.URLField(null=True)

    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.CASCADE,
        related_name='merchants',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Keyword(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    weight = models.IntegerField(default=1)

    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name='keywords',
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='keywords',
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    (models.Q(merchant__isnull=True) & models.Q(category__isnull=False)) |
                    (models.Q(merchant__isnull=False) & models.Q(category__isnull=True))
                ),
                name='check_either_merchant_or_category_and_only_one_is_null'
            )
        ]


ENRICHMENT_TRANSACTION_SQL = '''
    SELECT
        DISTINCT ON (t.id) t.id,
        t.id AS transaction_id,
        km.id AS merchant_id,
        COALESCE(km.category_id, k.category_id) AS category_id,
        k.id AS keyword_id

    FROM
        transactions_transaction t
        LEFT JOIN enrichment_category c ON c.type = SIGN(t.amount)
        LEFT JOIN enrichment_merchant m ON m.category_id = c.id

        LEFT JOIN enrichment_keyword k ON (
                k.category_id = c.id OR k.merchant_id = m.id
            )
            AND t.description ILIKE '%' || k.name || '%'

        LEFT JOIN enrichment_category kc  ON kc.id = k.category_id
        LEFT JOIN enrichment_merchant km  ON km.id = k.merchant_id

    ORDER BY
        t.id,
        k.weight DESC NULLS LAST;
'''


class EnrichmentTransaction(pg.View):

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name='enrichment',
    )

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='enrichments')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='enrichments')
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='enrichments')

    sql = ENRICHMENT_TRANSACTION_SQL

    class Meta:
        managed = False
