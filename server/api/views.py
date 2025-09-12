from typing import override

from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response


from server.payment.models import Payment, Collect, User
from server.api.serializers import (
    UserReadSerializer,
    UserCreateSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
    CollectSerializer,
)
from server.api.tasks import send_email_task


class CachedViewSetMixin:
    """Mixin for caching GET methods and updating data for them."""

    cache_timeout = 300

    def list(self, request, *args, **kwargs):
        """Caching list of instances."""
        key = f'{self.basename}:list'
        data = cache.get(key)
        if data:
            return Response(data)
        response = super().list(request, *args, **kwargs)
        cache.set(key, response.data, self.cache_timeout)
        print('success_caching')
        return response

    def retrieve(self, request, *args, **kwargs):
        """Cache one instance which was got by PK."""
        key = f'{self.basename}:detail:{kwargs['pk']}'
        data = cache.get(key)
        if data:
            return Response(data)
        response = super().retrieve(request, *args, **kwargs)
        cache.set(key, response.data, self.cache_timeout)
        print('success_caching')
        return response

    def perform_create(self, serializer):
        """Clear cache after creating new instance."""
        self._clear_cache(serializer.save())

    def perform_update(self, serializer):
        """Clear cache after updating instance."""
        self._clear_cache(serializer.save())

    def perform_destroy(self, serializer):
        """Clear cache after deleting instance."""
        self._clear_cache(serializer.save())

    def _clear_cache_for(self, basename: str, pk: int | None = None):
        """Delete cache after updating data."""
        cache.delete(f'{basename}:list')
        if pk:
            cache.delete(f'{basename}:retrieve:{pk}')


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()

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
    queryset = Payment.objects.all()

    @override
    def get_serializer_class(self):
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
    """ViewSet for Collect models with caching utils."""

    queryset = Collect.objects.all()
    serializer_class = CollectSerializer

    @override
    def perform_create(self, serializer: CollectSerializer) -> None:
        """Adding currect user during creating of new Collect."""
        collect = serializer.save(user=self.request.user)
        self._clear_cache_for('collect', collect.pk)
        send_email_task.delay('collect', collect.pk, self.request.user.email)
