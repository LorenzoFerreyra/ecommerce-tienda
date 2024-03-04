from .cart import Cart

# este un procesador de contexto para que el carrito figure en todos los templates de la tienda
# da datos adicionales a todos los templates
# se basa en la solicitud (request) actual.
def cart(request):
	# retornamos la data en forma de diccionario segun request actual
	return {'cart': Cart(request)}