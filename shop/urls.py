from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, initiate_payment, mpesa_callback

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('mpesa/stkpush/', initiate_payment, name='initiate_payment'),
    path('mpesa/callback/', mpesa_callback, name='mpesa_callback'),
]
