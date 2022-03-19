from django.contrib import admin
from django.urls import path, include
from .router import router


urlpatterns = [
    path('', include('frontend.urls')),
    path('api/v1/', include((router.urls, 'api'))),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('admin/', admin.site.urls),
]
