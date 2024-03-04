from store.models import Product, Profile

class Cart():
	def __init__(self, request):
		# el objeto session permite almacenar y recuperar datos de las sesiones de los usuarios
		self.session = request.session
		# obtenemos la solicitud
		self.request = request
		# hacemos un get de la key de la sesión actual (si el usuario está logueado)
		cart = self.session.get('session_key')

		# si el usuario es nuevo, no tiene key, por lo que debe crearla
		if 'session_key' not in request.session:
			cart = self.session['session_key'] = {}


		# se  asigna el contenido del carrito almacenado correspondiente a la sesión a la propiedad self.cart del objeto Cart.
		# así, el carrito estará disponible en todas las páginas de la web, porque self.cart es un atributo de la instancia de la clase Cart, que persiste a través de las solicitudes.
		self.cart = cart

	def db_add(self, product, quantity):
		product_id = str(product)
		product_qty = str(quantity)
		# Lógica para almacenar el ID de producto y su cantidad en el carrito
		if product_id in self.cart:
			pass
		else:
			
			self.cart[product_id] = int(product_qty)

		self.session.modified = True

		# Lógica para manejar los usuarios ya registrados
		if self.request.user.is_authenticated:
			# obtenemos el perfil del usuario registrado
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			carty = str(self.cart)
			carty = carty.replace("\'", "\"")
			# el objeto carty se guardará en el modelo Profile
			current_user.update(old_cart=str(carty))


	def add(self, product, quantity):
		product_id = str(product.id)
		product_qty = str(quantity)
		# lógica
		if product_id in self.cart:
			pass
		else:
			
			self.cart[product_id] = int(product_qty)

		self.session.modified = True

		# Lógica para manejar los usuarios ya registrados
		if self.request.user.is_authenticated:
			# obtenemos el perfil del usuario
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			
			carty = str(self.cart)
			carty = carty.replace("\'", "\"")
			# el objeto carty se guardará en el modelo Profile
			current_user.update(old_cart=str(carty))

	def cart_total(self):
		# obtenemos los ID de los productos para sacar el total
		product_ids = self.cart.keys()
		# buscamos en la db con esos ID
		products = Product.objects.filter(id__in=product_ids)
		# sacamos la cantidad del carrito
		quantities = self.cart
		# empezamos a contar desde 0
		total = 0
		
		for key, value in quantities.items():
			# convertimos en integer, entero, para calcular
			key = int(key)
			for product in products:
				if product.id == key:
					if product.is_sale:
						total = total + (product.sale_price * value)
					else:
						total = total + (product.price * value)



		return total



	def __len__(self):
		return len(self.cart)

	def get_prods(self):
		# sacamos los ID del carrito
		product_ids = self.cart.keys()
		# es el mismo proceso anterior pero para obtener nombres de producto
		products = Product.objects.filter(id__in=product_ids)

		# retornamos los productos obtenidos
		return products

	def get_quants(self):
		quantities = self.cart
		return quantities

	def update(self, product, quantity):
		product_id = str(product)
		product_qty = int(quantity)

		# obtenemosel carrito para hacer el update
		ourcart = self.cart
		# actualizamos
		ourcart[product_id] = product_qty

		self.session.modified = True
	

		# lógica de usuario
		if self.request.user.is_authenticated:
			# obtenemos profile en uso
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			
			carty = str(self.cart)
			carty = carty.replace("\'", "\"")
			# guardamos carty
			current_user.update(old_cart=str(carty))


		thing = self.cart
		return thing

	def delete(self, product):
		product_id = str(product)
		# borramos por product_id
		if product_id in self.cart:
			del self.cart[product_id]

		self.session.modified = True

		# lógica de usuario
		if self.request.user.is_authenticated:
			# obtenemos usuario actual
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			
			carty = str(self.cart)
			carty = carty.replace("\'", "\"")
			# guardamos carty a Profile
			current_user.update(old_cart=str(carty))