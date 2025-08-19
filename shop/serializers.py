from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product

        fields = [
            'id', 
            'name', 
            'description', 
            'price', 
            'stock', 
            'image',     
            'image_url',  
            'created_at'
        ]

    def get_image_url(self, obj):
        """
        Returns the full URL of the image from Cloudinary.
        """
       
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
       
        return None

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'