from django.contrib import admin
from .models import ShippingAddress


# registramos el modelo para que aparezca en la seccion de administrador
admin.site.register(ShippingAddress)

