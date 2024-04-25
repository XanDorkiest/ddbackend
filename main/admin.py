from django.contrib import admin
from .models import UserTable, \
    RoleTable, \
    CategoryTable, \
    TicketTable, \
    AssignmentTable, \
    ActionTable

# Register your models here.
admin.site.register(UserTable)
admin.site.register(RoleTable)
admin.site.register(CategoryTable)
admin.site.register(TicketTable)
admin.site.register(AssignmentTable)
admin.site.register(ActionTable)