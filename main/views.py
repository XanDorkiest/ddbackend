#from main.logic.historyLogic import historyLogic
from django.contrib.auth import authenticate
#from .logic import functionLogc
from django.db.models import Q
#from .logic.reservationLogic import reservationLogic
from django.shortcuts import get_object_or_404
from .auth import sessionCustomAuthentication
from .auth import roleClassify
from django.utils import timezone
from django.contrib.sessions.models import Session
from rest_framework.response import Response
from .models import UserTable, \
    RoleTable, \
    CategoryTable, \
    TicketTable, \
    AssignmentTable, \
    ActionTable
from django.conf import settings
from rest_framework.decorators import api_view, APIView, permission_classes
from .serializers import \
    RoleSerializer, UserSerializer, \
    CategorySerializer, TicketSerializer, \
    AssignmentSerializer, ActionSerializer, \
    UserInsertTableSerializer, changePassSerializer, FatAssignSerializer
from rest_framework import generics, status
from rest_framework import mixins

#authenticate
class LoginPoint(APIView):
    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            
            request.session['email'] = user.email
            request.session['role'] = user.role.role_name
            return Response({"message": "Login successful.","email": user.email,"role": user.role.role_name}, status.HTTP_200_OK)
        else:
            return Response({'error':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
@permission_classes([sessionCustomAuthentication])
def updatePass(request):
    if request.method == 'PUT':
        try:
            sessionemail = None
            if settings.DEBUG:
                sessionemail = request.data['email']
            else:
                sessionemail = request.session['email']
            old_password = request.data['old_password']

            new_password = request.data['new_password']
            new_password2 = request.data['user_password']

            if new_password != new_password2:
                return Response({'message':'password does not match'}, status=status.HTTP_409_CONFLICT)

            selectedData = get_object_or_404(UserTable, email=sessionemail)
            user = authenticate(request, email=sessionemail, password=old_password)
            if user and new_password2 == old_password:
                return Response({'message': 'New password matches old password'}, status=status.HTTP_400_BAD_REQUEST)

            if user is not None:
                serializer = changePassSerializer(selectedData, request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'password successfully changed'})
            else:
                return Response({'error': 'password does not match the old password'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)



@permission_classes([sessionCustomAuthentication])
class LogoutPoint(APIView):
    def delete(self, request, format=None):
        try:
            request.session.delete()
            response = Response(status=status.HTTP_200_OK)
            return response
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([sessionCustomAuthentication])
def logoutAllUsers(request):
    if request.method == 'DELETE':
        getRole = roleClassify()
        strRole = getRole.roleReturn(request)
        if strRole == "Super Admin":
            Session.objects.all().delete()
            return Response({'Message': 'All Users Logged out'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

#Class Based Views

#class based (Create, Update, Delete)
class RoleClass(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = RoleSerializer
    queryset = RoleTable.objects.all()
    roleLookup = roleClassify()

    def get(self, request):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Super Admin" or strRole == "Admin":
            return self.list(request)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def getRole(self, request):
        try:
            lookUpRole = self.roleLookup.roleReturn(request)
            return lookUpRole
        except:
            return ""

class CategoryClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = CategorySerializer
    queryset = CategoryTable.objects.all()
    lookup_field = 'category_id'
    roleLookup = roleClassify()

    def get(self, request, category_id=None):
        if category_id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Super Admin" or strRole == "Admin":
            return self.create(request)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


    def put(self, request, category_id=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Super Admin" or strRole == "Admin":
            return self.update(request, category_id)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, category_id=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Super Admin":
            return self.destroy(request, category_id)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class UsersClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = UserSerializer
    queryset = UserTable.objects.all()
    lookup_field = 'email'
    roleLookup = roleClassify()

    def get(self, request, email=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Super Admin" or strRole == "Admin":
            if email:
                return self.retrieve(request)
            else:
                return self.list(request)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Super Admin" or strRole == "Admin":
            serializer = UserInsertTableSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, email=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Super Admin":
            user = UserTable.objects.get(email=email)
            try:
                user.phone_number = request.data['phone_number']
            except:
                pass
            try:
                role = RoleTable.objects.get(role_id=request.data['role'])
                user.role = role
            except:
                pass
            user.save()
            return self.retrieve(request)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, email=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Super Admin":
            if email:
                return self.destroy(request, email)
            else:
                data = request.data
                deletionCount = 0
                for select in data:
                    try:
                        userObj = UserTable.objects.get(email=select['email'])
                        userObj.delete()
                        deletionCount += 1
                    except:
                        pass
                return Response({'message': 'Accounts Deleted',
                                 'accounts_deleted': str(deletionCount)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class OwnAssignedTicketsClass(generics.GenericAPIView):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = FatAssignSerializer
    queryset = AssignmentTable.objects.all()
    roleLookup = roleClassify()

    def get(self, request, email=None):
        email = email
        print(email)
        queryset = AssignmentTable.objects.filter(email=email)
        serializer = AssignmentSerializer(queryset, many=True)
        response = Response(serializer.data)
        return response
        

    def post(self, request):
        email = None
        if settings.DEBUG is False:
            email = request.session['email']
        else:
            email = request.data['email']
        serializer = AssignmentSerializer(self.get_queryset().filter(email=email), many=True)
        return Response(serializer.data)

    def getRole(self, request):
        try:
            lookUpRole = self.roleLookup.roleReturn(request)
            return lookUpRole
        except:
            return ""