from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import random
import string
import re
import json 
import base64

User = get_user_model()

def create_jwt_pair_tokens(user: User):
    refresh = RefreshToken.for_user(user)

    custom_data = {
        "user_id": user.id,
        "fullname": user.fullname,
        "username": user.username,
        "email": user.email,
        "is_profile_completed": user.is_profile_completed,
    }

    refresh['custom'] = custom_data

    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
    return tokens

def generate_token(token_length=20):
    characters = string.ascii_letters + string.digits 
    token = ''.join(random.choice(characters) for _ in range(token_length))
    return token

def email_validator(value:str) -> str:
    '''
    It takes email as input, return email if it is validated
    otherwise return will be None
    '''
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if not re.match(pat,value):
        raise ValidationError("This is not a valid email, try again!")
    return value

def decode_jwt_payload(token):
    try:
        _, payload_base64, _ = token.split('.')
        payload_bytes = base64.urlsafe_b64decode(payload_base64 + '==')
        payload_json = payload_bytes.decode('utf-8')
        return json.loads(payload_json)
    except ValueError:
        return None

def authenticate_user(request,role):
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return None

    if not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]
    # print('Token :: ',token)
    decoded_payload = decode_jwt_payload(json.loads(token).get('access'))
    if decoded_payload:
        # print('payload',decoded_payload)
        user_id = decoded_payload.get('user_id')
        try: 
            user = User.objects.get(id=user_id)
        except Exception as e : 
            return None

        if role=='user':
            return True
        elif role=='student' and user.role == 'student':
            return True
        elif role=='academic_counselor' and user.role == 'academic_counselor':
            return True
        elif role=='review_coordinator' and user.role == 'review_coordinator':
            return True
        elif role=='brototype_admin' and user.role == 'brototype_admin':
            return True
        elif role=='super_user' and user.role=='super_user' and user.is_superuser==True and user.is_staff==True:
            return True
        else:
            return None
    else:
        return None


def email_sender(email: str, link: str) -> bool:
    try:
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
                    <p>Click Sign in</p>
                    <a class="link-button" href="{link}">Sign In</a>
                    <p><strong>OR</strong></p>
                    <p>Follow this link to sign in to Bronet:</p>
                    <a href="{link}">{link}</a>
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
    except:
        return False
    else:
        return True
