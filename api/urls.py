from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FurnitureViewSet, SignupView, LoginView, LogoutView ,CheckoutView
from django.conf.urls.static import static
from django.conf import settings

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'furniture', FurnitureViewSet)

# The API URLs
urlpatterns = [
    path('', include(router.urls)),  # Furniture URLs
    path('signup/', SignupView.as_view(), name='signup'),  # Signup URL
    path('login/', LoginView.as_view(), name='login'),  # Login URL
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout URL
    path('checkout/', CheckoutView.as_view(), name='checkout'),  # Add the checkout URL
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)