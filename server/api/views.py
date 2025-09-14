from typing import override

from rest_framework import mixins, pagination, permissions, viewsets
from rest_framework.serializers import ModelSerializer

from server.api.cache_utils import CachedViewSetMixin
from server.api.permissions import AuthorOrReadOnly
from server.api.serializers import (
    CollectSerializer,
    PaymentCreateSerializer,
    PaymentSerializer,
    UserCreateSerializer,
    UserReadSerializer,
)
from server.api.tasks import send_email_task
from server.payment.models import Collect, Payment, User


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = pagination.PageNumberPagination

    @override
    def get_serializer_class(self) -> ModelSerializer:
        """Method for selecting serializer."""
        if self.action == 'create':
            return UserCreateSerializer
        return UserReadSerializer


class PaymentViewSet(
    CachedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for Payment model with caching utils."""

    queryset = Payment.objects.all()
    basename = 'payment'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = pagination.PageNumberPagination

    @override
    def get_serializer_class(
        self,
    ) -> PaymentCreateSerializer | PaymentSerializer:
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer

    @override
    def perform_create(self, serializer: PaymentCreateSerializer) -> None:
        """Adding currect user during creating of new Payment."""
        payment = serializer.save(user=self.request.user)
        self._clear_cache_for('payment', payment.pk)
        self._clear_cache_for('collect', payment.collect.pk)
        send_email_task.delay('payment', payment.pk, self.request.user.email)


class CollectViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    """ViewSet for Collect model with caching utils."""

    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = (AuthorOrReadOnly,)
    basename = 'collect'
    pagination_class = pagination.PageNumberPagination

    @override
    def perform_create(self, serializer: CollectSerializer) -> None:
        """Adding currect user during creating of new Collect."""
        collect = serializer.save(user=self.request.user)
        self._clear_cache_for('collect', collect.pk)
        send_email_task.delay('collect', collect.pk, self.request.user.email)
