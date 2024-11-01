from django.db import transaction
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from stocks.models import Holding, Transaction
from stocks.serializer import TransactionSerializer

# Create your views here.


class TransactionListCreate(ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        all_transactions = Transaction.objects.all()
        return all_transactions

    def perform_create(self, serializer):
        with transaction.atomic():
            transaction_instance = serializer.save(user=self.request.user)

            if transaction_instance.transaction_type == "buy":
                Holding.objects.create(
                    user=self.request.user,
                    stock=transaction_instance.stock,
                    quantity=transaction_instance.quantity,
                    cost=transaction_instance.price_per_share,
                    date=transaction_instance.date,
                )
