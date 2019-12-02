from rest_framework import serializers

from .utils import States, OrderCalculator


class OrderSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        self._order_calculator_class = OrderCalculator
        super().__init__(*args, **kwargs)

    price = serializers.FloatField(min_value=0.01)
    quantity = serializers.IntegerField(min_value=1)
    state_code = serializers.ChoiceField(choices=[(state.code, state.name) for state in States])
    total = serializers.SerializerMethodField()

    def get_total(self, validated_data):
        calculator = self._order_calculator_class(validated_data['price'],
                                                  validated_data['quantity'],
                                                  validated_data['state_code'])
        return calculator.taxed_price
