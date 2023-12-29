from rest_framework_bulk import BulkCreateAPIView

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionView(BulkCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
