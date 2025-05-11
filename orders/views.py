from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CartItem, Order, OrderItem
from .serializers import CartItemSerializer, OrderSerializer
from catalog.models import Product
from django.db.models import F
from django.db import transaction
import razorpay
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(user=user, total_price=total_price)

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        cart_items.delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PaymentInitiateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        user = request.user
        try:
            order = Order.objects.get(id=order_id, user=user, payment_status='pending')
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or already paid'}, status=404)

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        payment = client.order.create({
            'amount': int(order.total_price * 100),  # Razorpay uses paisa
            'currency': 'INR',
            'payment_capture': '1'
        })

        order.razorpay_order_id = payment['id']
        order.save()

        return Response({
            'order_id': order.id,
            'razorpay_order_id': payment['id'],
            'amount': order.total_price,
            'currency': 'INR'
        })

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def razorpay_webhook(request):
    data = request.data
    razorpay_order_id = data.get('payload', {}).get('payment', {}).get('entity', {}).get('order_id')
    razorpay_payment_id = data.get('payload', {}).get('payment', {}).get('entity', {}).get('id')

    try:
        order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        order.payment_status = 'paid'
        order.razorpay_payment_id = razorpay_payment_id
        order.save()
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)

    return Response({'status': 'Payment recorded'})
