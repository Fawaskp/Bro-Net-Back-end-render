from rest_framework.validators import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models.models import User, LoginWithEmailData,EmailChangeOtp
from .helpers import (
    email_validator,
    generate_token,
    email_sender,
    create_jwt_pair_tokens,
)
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .helpers import authenticate_user
from django.core.mail import send_mail
from django.conf import settings
import random
import re

"""
check-username
token
is_user_auth
is_user_auth
LoginWithEmail
LoginWithSocialMedia
"""

block_message = "You can't login, your account is blocked"

@api_view(["GET"])
@csrf_exempt
def check_username(request, username):
    if username:
        regex_pattern = r"^[a-zA-Z0-9_.-]+$"
        if not re.match(regex_pattern, username):
            return Response(data={"message": "Invalid username format", "status": 400})
        is_exist = User.objects.filter(username=username).exists()
        if is_exist:
            return JsonResponse(
                data={"message": "given username already exist", "status": 409}
            )
        else:
            return JsonResponse(data={"message": "username is acceptable"}, status=202)
    else:
        return JsonResponse(data={"message": "username is important", "status": 400})


@api_view(["GET"])
def get_user_id_by_username(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse(data={"message": "user not found", "status": 404})
    else:
        return JsonResponse(data={"message": "success", "id": user.id, "status": 200})


@api_view(["POST"])
@csrf_exempt
def token(request):
    if request.method == "POST":
        email = request.data.get("email")
        if email:
            try:
                userInstance = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(data={"message": "Something went wrong", "status": 404})
            else:
                token = create_jwt_pair_tokens(userInstance)
                return Response(data={"token": token}, status=202)
        else:
            return Response(data={"message": f"email is important", "status": 400})
    else:
        return Response(data={"detail": f"{request.method} is not allowed"}, status=405)


@api_view(["POST"])
@csrf_exempt
def is_user_auth(request):
    isVerified = authenticate_user(request, "user")
    return JsonResponse(isVerified is not None, safe=False)


@api_view(["POST"])
@csrf_exempt
def is_su_auth(request):
    isVerified = authenticate_user(request, "super_user")
    print("su verification", isVerified)
    return JsonResponse(isVerified is not None, safe=False)


class LoginWithEmail(APIView):
    def get(self, request):
        token = request.GET.get("token")

        if not token:
            return Response(
                data={"message": "token didn't get with request", "status": 400}
            )
        try:
            login_instance = LoginWithEmailData.objects.get(token=token)
        except LoginWithEmailData.DoesNotExist:
            return Response(data={"message": "Enter Valid Link", "status": 400})

        email = login_instance.email
        elapsed_minutes = login_instance.get_time_elapsed()

        if elapsed_minutes <= 5:
            email_exist = User.objects.filter(email=email).exists()
            if not email_exist:
                username = email.split("@")[0]
                user = User.objects.create_user(
                    email=email, password=email, username=username
                )
            else:
                user = User.objects.get(email=email)
                if not user.is_active:
                    return Response(
                        data={
                            "message": block_message,
                            "is_profile_completed": user.is_profile_completed,
                            "status": 403,
                        }
                    )

            login_instance.delete()
            return Response(
                data={
                    "Token": create_jwt_pair_tokens(user),
                    "is_profile_completed": user.is_profile_completed,
                    "status": 200,
                }
            )
        else:
            login_instance.delete()
            return Response(data={"message": "Your Link is expired", "status": 400})

    def post(self, request):
        email = request.data.get("email")
        try:
            email_validator(email)
        except ValidationError:
            return Response(data={"message": f"Enter Valid Email"})

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response(data={"message": block_message, "status": 403})

        token = generate_token()
        link = f"http://localhost:5173/auth/login/?token={token}"
        result = email_sender(email, link)
        if result:
            LoginWithEmailData.objects.create(token=token, email=email)
            return Response(data={"token": token, "status": status.HTTP_200_OK})
        else:
            return Response(
                data={
                    "message": "Email couldn't send",
                    "status": status.HTTP_503_SERVICE_UNAVAILABLE,
                }
            )


class LoginWithSocialMedia(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            email_validator(email)
        except ValidationError:
            return Response(data={"message": f"There is an issue with provided E-mail"})

        email_exist = User.objects.filter(email=email).exists()

        if not email_exist:
            username = email.split("@")[0]
            user = User.objects.create_user(
                email=email, password=email, username=username
            )
        else:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response(
                    data={
                        "message": block_message,
                        "is_profile_completed": user.is_profile_completed,
                        "status": 403,
                    }
                )

        return Response(
            data={
                "Token": create_jwt_pair_tokens(user),
                "is_profile_completed": user.is_profile_completed,
                "status": 200,
            }
        )

@api_view(['POST'])
def send_otp_for_change_mail(request):
    email = request.data.get('email')
    username = request.data.get('username')
    if User.objects.filter(email=email).exists():
        return Response(status=400,data={"message":"email already exist"})
    try:
        user = User.objects.get(username=username)
    except:
        return Response(status=400,data={"message":"Send correct user id"})
        
    otp = "".join(str(random.randint(0, 9)) for _ in range(4))
    EmailChangeOtp.objects.create(user=user,new_email=email,otp=otp)
    html_message = f'''
    <html>
        <head>
            <style>                    
                .container {{
                    background-color: white;
                    color:#242424;
                    padding: 20px;
                    border-radius: 5px;
                    display: inline-block;
                    text-align: left;
                }}
                
                .link-button {{
                    display: inline-block;
                    background-color: #6366F1;
                    color: #ffffff!important;
                    text-decoration: none;
                    padding: 10px 20px;
                    border-radius: 3px;
                }}
                
                a {{
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Hi from Bronet</h1>
                <p>Here is your OTP for change E-mail</p>
                <p><strong> OTP : {otp}</strong></p>
            </div>
        </body>
    </html>
    '''

    send_mail(
        "Hi from Bronet",
        '',
        settings.EMAIL_HOST_USER,
        [email],
        html_message=html_message,
        fail_silently=False,
    )
    return Response(status=200,data={'message':'Send OTP to mail'})

@api_view(['POST'])
def verify_otp_for_change_mail(request):
    otp = request.data.get('otp')
    username = request.data.get('username')
    try:
        user = User.objects.get(username=username)
        otp_instance = EmailChangeOtp.objects.get(user=user,otp=otp)
        new_email = otp_instance.new_email
        otp_instance.delete()
        user.email = new_email
        user.save()
    except Exception as e:
        return Response(status=400,data={"message":f"{e}"})
    
    return Response(status=200,data={'message':'Verified'})

