from datetime import date
from django.contrib.auth.backends import BaseBackend
from main.models import UserTable
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

class roleClassify():
    def roleReturn(self, request):
        debug = settings.DEBUG
        if debug:
            return "Super Admin"
        role = request.session['role_name']
        return role

class sessionCustomAuthentication(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            debug = settings.DEBUG
            if debug:
                return True
            email = request.session['email']
            return True
        except:
            return False

class userAuth(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        entered_Password = password
        hasher = PBKDF2PasswordHasher()
        try:
            user = UserTable.objects.get(email=email)
            if hasher.verify(entered_Password, user.password):
                print(user)
                return user
            else:
                return None
        except UserTable.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserTable.objects.get(email=user_id)
        except UserTable.DoesNotExist:
            return None

class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Set the Access-Control-Allow-Origin header to the domain of the incoming request
        origin = request.headers.get('Origin')
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Headers'] = 'content-type'

        # Allow credentials to be sent with the request
        response['Access-Control-Allow-Credentials'] = 'true'

        return response