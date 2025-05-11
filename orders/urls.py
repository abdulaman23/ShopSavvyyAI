from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, OrderViewSet
from .views import PaymentInitiateView, razorpay_webhook

router = DefaultRouter()
router.register('cart', CartItemViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('pay/<int:order_id>/', PaymentInitiateView.as_view(), name='initiate-payment'),
    path('webhook/razorpay/', razorpay_webhook, name='razorpay-webhook'),
]
