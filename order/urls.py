from django.urls import path

from . import api

app_name = 'order'

urlpatterns = [
    path('orders/', api.TotalOrderPrice.as_view(), name='order-price-handler'),
]
