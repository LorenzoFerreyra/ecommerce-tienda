from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile, OrderItem
from django.contrib.auth.models import User

# registramos modelos en la seccion de admin
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(OrderItem)

# Mostrar User y Profile en la misma página que la información del usuario.
class ProfileInline(admin.StackedInline):
	model = Profile

# el objetivo es que cuando se vea o edite un User en el panel de administración,
# también se mostrará y se podrá editar su perfil en la misma página.
class UserAdmin(admin.ModelAdmin):
	model = User
	field = ["username", "first_name", "last_name", "email"]
	inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)

