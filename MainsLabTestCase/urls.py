from django.contrib import admin
from django.urls import path, include
from billing.routers import router as billing_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(billing_router.urls))
]
