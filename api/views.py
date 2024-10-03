from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from django.conf import settings
from django.utils.html import format_html
from .models import Furniture, UserProfile
from .serializers import FurnitureSerializer
from django.http import JsonResponse
import json
import os
from rest_framework.decorators import api_view

class FurnitureViewSet(viewsets.ModelViewSet):
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        mobile_no = request.data.get('mobile_no')  # New field
        address = request.data.get('address')        # New field

        # Validate inputs
        if not username or not password or not email or not mobile_no or not address:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )

            UserProfile.objects.create(user=user, mobile_no=mobile_no, address=address)

            user_profile_data = {
                'username': username,
                'email': email,
                'mobile_no': mobile_no,
                'address': address,
            }
            file_path = r'D:\Projects\FurnitureMart\frontend\src\api\profile.json'

            with open(file_path, 'w') as json_file:
                json.dump(user_profile_data, json_file)

            html_message = format_html('''\
            <div style="font-family: 'Arial', sans-serif; padding: 20px; max-width: 600px; margin: auto; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #ff6b6b; text-align: center; font-size: 24px;">
                    Welcome to 
                    <strong style="color: #ff6b6b;">FurnitureMart</strong>
                </h1>
                <p style="color: black; font-size: 16px; line-height: 1.5;">
                    Hello {username},<br><br>
                    Thank you for signing up with <strong>FurnitureMart</strong>! We're excited to have you on board. Your registration was successful, and you're now part of our growing community.
                </p>
                <p style="color: black; font-size: 16px; line-height: 1.5;">
                    Explore our exclusive collection and enjoy personalized furniture recommendations just for you.
                </p>
                <p style="text-align: center; margin-top: 20px;">
                    <a href="https://furnituremart.com/login" style="background-color: #ff6b6b; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-size: 16px;">
                        Get Started
                    </a>
                </p>
                <p style="color: black; font-size: 12px; text-align: center; margin-top: 40px;">
                    If you didn't sign up for FurnitureMart, please ignore this email.
                </p>
            </div>
            ''', username=username)

            # Send confirmation email
            send_mail(
                'Welcome to FurnitureMart',
                'Thank you for signing up with FurnitureMart! Your registration was successful.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=html_message,
            )

            return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)

        except BadHeaderError:
            return Response({'error': 'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)
        except SMTPException as e:
            return Response({'error': f'Error sending email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate inputs
        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)

class CheckoutView(APIView):
    def post(self, request):
        try:
            # Use DRF's request.data to automatically parse JSON
            data = request.data
            user_email = data.get('email')
            name = data.get('name')
            address = data.get('address')
            mobile_no = data.get('totalAmount')  # Assuming totalAmount is actually the price

            # Validate the email
            if not user_email:
                return Response({'status': 'error', 'message': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Prepare the HTML email message
            html_message = format_html('''\
            <div style="font-family: 'Arial', sans-serif; padding: 20px; max-width: 600px; margin: auto; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #ff6b6b; text-align: center; font-size: 24px; margin-bottom: 20px;">
                    Order Confirmation
                </h1>
                <p style="color: #333333; font-size: 16px; line-height: 1.5;">
                    Dear <strong>{name}</strong>,<br><br>
                    Thank you for your order! We appreciate your business.
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.5;">
                    <strong>Delivery Details:</strong><br>
                    Address: <span style="color: #555555;">{address}</span><br>
                    <strong>Total Price:</strong> <span style="color: #555555;">{mobile_no}</span>
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.5;">
                    We will notify you once your order is shipped. If you have any questions, feel free to contact us.
                </p>
                <p style="color: #777777; font-size: 12px; text-align: center; margin-top: 40px;">
                    If you didn't make this order, please ignore this email.
                </p>
            </div>
            ''', name=name, address=address, mobile_no=mobile_no)

            subject = 'Order Confirmation'
            recipient_list = [user_email]

            # Send email with HTML content
            send_mail(
                subject,
                message='',  # No plain text message
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_message,  # Send the HTML message
                fail_silently=False
            )

            return Response({'status': 'success', 'message': 'Order confirmation email sent successfully.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
