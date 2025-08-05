from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from .mpesa import lipa_na_mpesa
import traceback


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        orders = Order.objects.filter(products=instance)
        for order in orders:
            order.products.remove(instance)

        instance.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer


@api_view(['POST'])
def initiate_payment(request):
    phone = request.data.get('phone')
    amount = request.data.get('amount')

    if not phone or not amount:
        return Response({'error': 'Phone and amount are required.'}, status=400)

    try:
        print(f"📞 Initiating STK Push for phone={phone}, amount={amount}")
        response = lipa_na_mpesa(phone, amount)
        print("✅ M-Pesa STK Push Response:", response)
        return Response(response)
    except Exception as e:
        print("❌ M-Pesa STK Push Error:")
        traceback.print_exc()
        return Response({'error': f"Payment failed: {str(e)}"}, status=500)


@csrf_exempt
@api_view(['POST'])
def mpesa_callback(request):
    print("✅ M-Pesa Callback received:")
    print(request.data)
    return Response({"message": "Callback received"}, status=200)
