
from django.contrib import admin
from .models import Customer, Appointment, Review, Service, PortfolioItem

# Customize the admin site headers
admin.site.site_header = "Dorah's Salon Admin"
admin.site.site_title = "Dorah's Salon Admin Portal"
admin.site.index_title = "Welcome to Dorah's Salon Admin Portal"

# Register your models here
admin.site.register(Customer)
admin.site.register(Appointment)
admin.site.register(Review)
admin.site.register(Service)
admin.site.register(PortfolioItem)
