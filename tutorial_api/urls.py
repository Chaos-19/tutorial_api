from django.urls import include, path
from rest_framework import routers
from django.contrib import admin



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include("src.urls")),
    path('', include("quiz.urls")),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
