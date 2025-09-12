from rest_framework.routers import DefaultRouter

from server.api.views import UserViewset, PaymentViewSet, CollectViewSet


router = DefaultRouter()
router.register(
    'users',
    UserViewset,
    basename='user',
)
router.register(
    'payments',
    PaymentViewSet,
    basename='payment',
)
router.register(
    'collects',
    CollectViewSet,
    basename='collect',
)
