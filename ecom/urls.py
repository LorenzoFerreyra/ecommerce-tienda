from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
settings.MEDIA_URL es el prefijo que se usa para construir las rutas a los archivos multimedia (media files) en el servidor.
Si settings.MEDIA_URL es /media/, entonces un archivo con la ruta /media/images/producto.jpg sería accesible a través de la URL /media/images/producto.jpg en el navegador.
Por otro lado, settings.MEDIA_ROOT es la ubicación física en el sistema de archivos donde se almacenan los archivos de medios. Django sirve estos archivos estáticos automáticamente cuando DEBUG es True en settings.py.


"""