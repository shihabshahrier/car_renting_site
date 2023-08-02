from django.contrib import admin
from .models import Car, Driver, Rent, Review, Garage, Customer

# Register your models here.
admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(Rent)
admin.site.register(Review)
admin.site.register(Garage)
admin.site.register(Customer)

