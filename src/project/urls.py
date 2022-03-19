from django.contrib import admin
from django.urls import path, include
from .routers import router_v1


urlpatterns = [
    path('', include('frontend.urls')),
    path('api/v1/', include((router_v1.urls, 'api_v1'))),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('admin/', admin.site.urls),
]
