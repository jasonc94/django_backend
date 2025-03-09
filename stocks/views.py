from decimal import Decimal
from django.db import transaction
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from stocks.models import Holding, InvestmentReturn, Transaction
from stocks.serializer import TransactionSerializer
from django.contrib.auth.models import User

# Create your views here.


class TransactionListCreate(ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.all()

    def perform_create(self, serializer):
        with transaction.atomic():
            auth_user = User.objects.get(pk=1)
            transaction_instance = serializer.save(user=auth_user)
            updateHolding(transaction_instance, auth_user)


def updateHolding(transaction_instance, user):
    if transaction_instance.transaction_type == "buy":
        Holding.objects.create(
            user=user,
            transaction=transaction_instance,
            stock=transaction_instance.stock,
            quantity=transaction_instance.quantity,
            cost=transaction_instance.price_per_share,
            date=transaction_instance.date,
            remaining_quantity=transaction_instance.quantity,
        )
    else:
        selling_quantity = transaction_instance.quantity
        holdings = Holding.objects.filter(
            user=user, stock=transaction_instance.stock, remaining_quantity__gt=0
        ).order_by("date")

        for holding in holdings:
            if selling_quantity == 0:
                break
            quantity_to_sell = min(holding.remaining_quantity, selling_quantity)
            selling_quantity -= quantity_to_sell
            holding.remaining_quantity -= quantity_to_sell
            holding.save()
            updateInvestment(
                holding, transaction_instance, user, Decimal(quantity_to_sell)
            )


def updateInvestment(holding, transaction_instance, user, sold_quantity):
    holding_period = transaction_instance.date - holding.date
    cost_basis = holding.cost * sold_quantity
    sale_proceeds = transaction_instance.price_per_share * sold_quantity
    gain = sale_proceeds - cost_basis
    investment_type = "long-term" if holding_period.days > 365 else "short-term"
    InvestmentReturn.objects.create(
        user=user,
        holding=holding,
        stock=transaction_instance.stock,
        purchase_date=holding.date,
        sell_date=transaction_instance.date,
        investment_type=investment_type,
        gain_loss_amount=gain,
    )
