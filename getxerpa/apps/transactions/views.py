from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionView(CreateAPIView):
    queryset = Transaction.objects.select_related('enrichment')
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        queryset = self.perform_create(serializer)

        serializer_output = TransactionSerializer(queryset, many=True)

        category_enrichment = 0
        merchant_enrichment = 0

        for transaction in serializer_output.data:
            if transaction['enrichment']['category_id'] is not None:
                category_enrichment += 1

            if transaction['enrichment']['merchant_id'] is not None:
                merchant_enrichment += 1

        data = {
            'count': len(serializer_output.data),
            'category_enrichment': category_enrichment,
            'merchant_enrichment': merchant_enrichment,
            'transactions': serializer_output.data
        }

        return Response(data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        batch = [Transaction(**item) for item in serializer.validated_data]
        return Transaction.objects.bulk_create(batch)
