from rest_framework.serializers import ModelSerializer
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from .models import Transaction


class TransactionSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta(object):
        model = Transaction
        fields = '__all__'
        list_serializer_class = BulkListSerializer


