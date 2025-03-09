from rest_framework import serializers

from stocks.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "user",
            "stock",
            "transaction_type",
            "quantity",
            "price_per_share",
            "date",
        )
        read_only_fields = ["user"]


class PortfolioSerializer(serializers.Serializer):
    ticker = serializers.CharField()
    company_name = serializers.CharField()
    total_quantity = serializers.FloatField()
    average_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
