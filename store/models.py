from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Modelo para perfil
# notar que cada instancia de Profile está asociada con exactamente una instancia de User y viceversa.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_modified = models.DateTimeField(User, auto_now=True)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True)
	state = models.CharField(max_length=200, blank=True)
	zipcode = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True)
	# old_cart se usa para mantener un registro del carrito de compras del usuario antes de que se cree el perfil
	old_cart = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.user.username

# se crea un perfil por default cuando el usuario se registra
	
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

post_save.connect(create_profile, sender=User)
"""
La función create_profile es un "callback" que se ejecuta cada vez que se crea una instancia de User.
Crea automáticamente un perfil asociado con el usuario cuando se crea el usuario.
Esto se hace con el método post_save de la señal signals de Django.
Cuando se crea un User, se envía una señal post_save que se captura mediante create_profile,
y se crea un Profile asociado con el User que se acaba de crear.
"""






# nuestras categorías de productos
class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	# el plural correcto de categorías
	class Meta:
		verbose_name_plural = 'categories'


# Customers
class Customer(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)


	def __str__(self):
		return f'{self.first_name} {self.last_name}'



# clase producto
class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	description = models.CharField(max_length=250, default='', blank=True, null=True)
	image = models.ImageField(upload_to='uploads/product/')
	# campos para hacer promociones y liquidaciones de prodcto
	is_sale = models.BooleanField(default=False)
	sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

	def __str__(self):
		return self.name


# orden de compra
class Order(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	address = models.CharField(max_length=100, default='', blank=True)
	phone = models.CharField(max_length=20, default='', blank=True)
	date = models.DateField(default=datetime.datetime.today)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.product