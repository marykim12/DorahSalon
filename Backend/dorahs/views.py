from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import *

# Create your views here.
def index (request):
    return render(request,'index.html')
class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_serializer = CustomerSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            return Response({
                "user": user_serializer.data,
                "message": "User registered successfully!"
            }, status=status.HTTP_201_CREATED)
        return Response({
            "errors" : user_serializer.errors,
            "message": "User registration failed."
        }, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_admin'] = user.is_staff  # Add admin status as a claim
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_admin'] = self.user.is_staff  # Add to the response body
        if not self.user.is_staff:
            try:
                customer = self.user.customer
                data['customer_id'] = customer.customer_id
            except Customer.DoesNotExist:
                raise serializers.ValidationError("Customer profile not found.")
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = IsAuthenticated(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_admin': user.is_staff,  # Include admin status
            }

            if not user.is_staff:  # Non-admin users should have a customer profile
                try:
                    customer = user.customer  # Assuming a OneToOne relationship with Customer
                    response_data['customer_id'] = customer.customer_id
                except Customer.DoesNotExist:
                    return Response({"error": "Customer profile not found."}, status=status.HTTP_404_NOT_FOUND)

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
    def perform_update(self, serializer):
        serializer.save()
    def perform_destroy(self, instance):
        instance.delete()


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
    def perform_update(self, serializer):
        serializer.save()
    def perform_destroy(self, instance):
        instance.delete()


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['customer__name', 'appointment_date']
    search_fields = ['customer__name', 'decription']

    def perform_create(self, serializer):
        serializer.save()
    def perform_update(self, serializer):
        serializer.save()
    def perform_destroy(self, instance):
        instance.delete()

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['customer__name', 'approved']
    search_fields = ['customer__name', 'content']

    def perform_create(self, serializer):
        serializer.save()
    
    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']

    def perform_create(self, serializer):
        serializer.save()
    
    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()
class PortfolioItemViewSet(viewsets.ModelViewSet):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['media_type']
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save()
    
    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()