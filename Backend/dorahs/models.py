from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15,blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    email = models.EmailField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointments')
    decription = models.TextField("service Description", blank=True, null=True)
    image = models.ImageField(upload_to="appointment Image", blank=True, null=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    help_text="Upload reference image (optional)"
    appointment_date = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer}'s appointment is on {self.appointment_date}"
    
class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.customer.name} ({self.rating} stars)"
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()  # e.g., timedelta(minutes=30)
    price = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('hair', 'Hair'),
        ('dreadlocks', 'Dreadlocks'),
        ('nails', 'Nails'),
        ('skincare', 'Skincare'),
        ('other', 'Other')
    ])
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} (${self.price})"
    
class PortfolioItem(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('before_after', 'Before/After')
    ]
    
    title = models.CharField(max_length=100)
    media_type = models.CharField(max_length=12, choices=MEDIA_TYPE_CHOICES)
    image = models.ImageField(upload_to='portfolio/images/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)  # For YouTube/Vimeo links
    before_image = models.ImageField(upload_to='portfolio/before/', null=True, blank=True)
    after_image = models.ImageField(upload_to='portfolio/after/', null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()})"
