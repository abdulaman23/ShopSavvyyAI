from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, OrderViewSet

router = DefaultRouter()
router.register('cart', CartItemViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
]
