from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path(r"", include("puput.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
