from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    CustomerViewSet,
    AppointmentViewSet,
    ReviewViewSet,
    ServiceViewSet,
    CustomTokenObtainPairView,
    RegisterUserView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'services', ServiceViewSet)

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/register/', RegisterUserView.as_view(), name='register_user'),
    path('', include(router.urls)),
]
