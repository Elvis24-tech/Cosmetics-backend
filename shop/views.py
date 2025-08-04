from rest_framework import viewsets
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .mpesa import lipa_na_mpesa


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@api_view(['POST'])
def initiate_payment(request):
    phone = request.data.get('phone')
    amount = request.data.get('amount')

    if not phone or not amount:
        return Response({'error': 'Phone and amount are required.'}, status=400)

    try:
        response = lipa_na_mpesa(phone, amount)
        return Response(response)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['POST'])
def mpesa_callback(request):
    print("M-Pesa Callback received:", request.data)
    return Response({"message": "Callback received"}, status=200)
