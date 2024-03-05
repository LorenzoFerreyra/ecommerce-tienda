from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal



# Modelo para perfil
# notar que cada instancia de Profile está asociada con exactamente una instancia de User y viceversa.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_modified = models.DateTimeField(User, auto_now=True)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True, default="Huanuco")
	state = models.CharField(max_length=200, blank=True, default="Huanuco")
	zipcode = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True, default="Peru")
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
    id = models.AutoField(primary_key=True, editable=False)    
    first_name = models.CharField(max_length=50, default="Cliente")
    last_name = models.CharField(max_length=50, default="Al mostrador")
    dni = models.IntegerField()
    email = models.EmailField(max_length=100, blank=True)
    address = models.CharField(max_length=250, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(default=0,
        validators = [MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_subtotal(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity