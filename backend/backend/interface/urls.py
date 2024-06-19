"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

from backend.interface.job.urls import router as jobs_router
from backend.interface.user.urls import router as users_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url="admin/", permanent=False)),
    path(f"{settings.COMMON_URL}", include(users_router.urls)),
    path(f"{settings.COMMON_URL}", include(jobs_router.urls)),
    path(f"{settings.COMMON_URL}schema/",
         SpectacularAPIView.as_view(), name="schema"),
    path(
        f"{settings.COMMON_URL}schema/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="spec_schema",
    ),
    path("refresh/token/", TokenRefreshView.as_view(), name="refresh_token"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
