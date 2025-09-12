from django.core import cache
from rest_framework.response import Response


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
