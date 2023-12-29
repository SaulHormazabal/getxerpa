from rest_framework import serializers

from getxerpa.apps.enrichment.models import EnrichmentTransaction

from .models import Transaction


class EnrichmentTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnrichmentTransaction
        fields = (
            'merchant_id',
            'category_id',
        )


class TransactionSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField()
    enrichment = EnrichmentTransactionSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
