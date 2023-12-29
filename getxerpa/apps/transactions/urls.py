from django.urls import path

from .views import TransactionView

urlpatterns = [
    path('api/transactions/bulk-create/', TransactionView.as_view()),
]
