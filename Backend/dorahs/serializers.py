from .models import Customer, Appointment, Review, Service, PortfolioItem
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'validators': []}  # Disable unique validation for email
        }
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
# Custom JWT serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        # Assuming user has a 'profile' with a 'role' field
        if hasattr(user, 'profile') and hasattr(user.profile, 'role'):
            token['role'] = user.profile.role
        return token
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone_number', 'email']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'validators': []}  # Disable unique validation for email
        }
    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        customer = Customer.objects.create(**validated_data)
        if user_data:
            user = User.objects.create_user(username=user_data['username'], email=user_data['email'], password=user_data['password'])
            customer.user = user
            customer.save()
        return customer

class AppointmentSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'decription', 'image', 'appointment_date', 'is_confirmed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    def create(self, validated_data):
        customer_data = validated_data.pop('customer', None)
        appointment = Appointment.objects.create(**validated_data)
        if customer_data:
            customer = Customer.objects.create(**customer_data)
            appointment.customer = customer
            appointment.save()
        return appointment
    

class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'customer', 'content', 'rating', 'approved', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        customer_data = validated_data.pop('customer', None)
        review = Review.objects.create(**validated_data)
        if customer_data:
            customer = Customer.objects.create(**customer_data)
            review.customer = customer
            review.save()
        return review
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'duration', 'price', 'category', 'is_active']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        service = Service.objects.create(**validated_data)
        return service
    
class PortfolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = ['id', 'title', 'media_type', 'image', 'video', 'before_after_image']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        portfolio_item = PortfolioItem.objects.create(**validated_data)
        return portfolio_item
    