from django.apps import AppConfig

# acá definimos la configuración específica de la aplicación cart
# es una subclase de AppConfig,
# una clase base proporcionada por Django para definir configuraciones de aplicación
# nosotros creamos un carrito para la tienda
class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
