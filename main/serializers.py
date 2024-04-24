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
# class specialInventorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InventoryTable
#         fields = '__all__'
#         depth = 1

# class specialHistorySerializer(serializers.ModelSerializer):
#     item_code = ReservationHistoryExtSerializer()
#     email = HistoryReportExtUserTable()
#     class Meta:
#         model = HistoryTable
#         fields = '__all__'

# class specialReservationSerializer(serializers.ModelSerializer):
#     item_code = ReservationHistoryExtSerializer()
#     class Meta:
#         model = ReservationTable
#         fields = '__all__'

# class numberOnlyUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserTable
#         fields = ['email','phone_number']

# class itemNameOnlySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InventoryTable
#         fields = ['item_name']

# class textPeopleFindSerializer(serializers.ModelSerializer):
#     email = numberOnlyUserSerializer()
#     item_code = itemNameOnlySerializer()
#     class Meta:
#         model = HistoryTable
#         fields = ['email', 'item_code','due_date']

# class specialHistoryReportSerializer(serializers.ModelSerializer):
#     item_code = ReservationHistoryExtSerializer()
#     email = HistoryReportExtUserTable()
#     class Meta:
#         model = HistoryTable
#         fields = '__all__'

# class multipleItemInsertSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InventoryTable
#         fields = ['category','item_name','item_condition','status']

# class multipleItemUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InventoryTable
#         fields = ['item_code','category','item_name','item_condition','status']

# class pendingReservationSerializer(serializers.ModelSerializer):
#     item_code = pendingExtReservation()
#     class Meta:
#         model = ReservationTable
#         fields = ['reservation_id','item_code','date_of_expiration']

# class changePassSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserTable
#         fields = ['user_password']

# class extspecificUserHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InventoryTable
#         fields = ['item_code','item_name']

# class specificUserHistorySerializer(serializers.ModelSerializer):
#     item_code = extspecificUserHistorySerializer()
#     class Meta:
#         model = HistoryTable
#         fields = ['item_code','date_in','date_out']

# class specificUserReservationSerializer(serializers.ModelSerializer):
#     item_code = extspecificUserHistorySerializer()
#     class Meta:
#         model = ReservationTable
#         fields = ['reservation_id','item_code','date_of_expiration']

# class UserInsertTableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserTable
#         fields = ['email','phone_number','first_name','last_name','role','user_password']