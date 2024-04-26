from rest_framework import serializers
from .models import UserTable, \
    RoleTable, \
    CategoryTable, \
    TicketTable, \
    AssignmentTable, \
    ActionTable

#nested serializer
class FKeyEmailSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserTable
        
        fields = '[email]'


#base serializers
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleTable
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryTable
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTable
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentTable
        fields = '__all__'

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionTable
        fields = '__all__'



#specialz serializers

class changePassSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['user_password']

class UserInsertTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['email','phone_number','first_name','last_name','role','user_password']

class FatAssignSerializer(serializers.ModelSerializer):
    ticket_subject = serializers.CharField(source='ticket_id.ticket_subject')
    ticket_description = serializers.CharField(source='ticket_id.ticket_description')
    ticket_status = serializers.CharField(source='ticket_id.status')
    ticket_creation_date = serializers.DateField(source='ticket_id.creation_date')
    user_email = serializers.EmailField(source='email.email')
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = AssignmentTable
        fields = ['assignment_id', 'ticket_id', 'ticket_subject', 'ticket_description', 'ticket_status', 'ticket_creation_date', 'user_email', 'user_name']

    def get_user_name(self, obj):
        return f"{obj.email.first_name} {obj.email.last_name}"