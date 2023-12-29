from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from getxerpa.config.urls import urlpatterns


urlpatterns += [
    path('', RedirectView.as_view(url='/api/', permanent=True)),
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
