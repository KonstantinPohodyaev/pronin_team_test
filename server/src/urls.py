from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from server.api.urls import router as api_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'auth/token',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'auth/token/refresh',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path('api/', include(api_router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
    )
