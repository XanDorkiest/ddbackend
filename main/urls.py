from django.urls import path
from .views import updatePass, UsersClass, \
LoginPoint, LogoutPoint, \
logoutAllUsers, OwnAssignedTicketsClass

urlpatterns = [
    path('userChangePassword/', updatePass),
    path('user/<str:email>', UsersClass.as_view()),
    path('user/', UsersClass.as_view()),

    path('login/', LoginPoint.as_view()),
    path('logout/', LogoutPoint.as_view()),
    path('logoutAllUsers/', logoutAllUsers),
    path('changePass/', updatePass),

    path('ownTickets/<str:email>', OwnAssignedTicketsClass.as_view())
]