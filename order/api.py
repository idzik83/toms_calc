from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import OrderSerializer


class TotalOrderPrice(GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
