from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from server.api.urls import router as api_router



urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'auth/token',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'auth/token/refresh',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path('api/', include(api_router.urls)),
]
