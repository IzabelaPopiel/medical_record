from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('medrecord/', include('medrecord.urls')),
    path('admin/', admin.site.urls),
]