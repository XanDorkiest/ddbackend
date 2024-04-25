from django.utils import timezone
from django.db import models
from django.contrib.auth.hashers import PBKDF2PasswordHasher

class RoleTable(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=45)

    def __str__(self):
        return self.role_name

    class Meta:
        managed = False
        db_table = 'role_table'

class UserTable(models.Model):
    email = models.CharField(primary_key=True, max_length=200)
    role = models.ForeignKey(RoleTable, models.DO_NOTHING)
    phone_number = models.BigIntegerField()
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.password:
            self.password = PBKDF2PasswordHasher().encode(self.password, PBKDF2PasswordHasher().salt())
        super().save(*args, **kwargs)


    def __str__(self):
        stringFormat = "{email} : {firstName} {lastName} : {role}"
        return stringFormat.format(email=self.email,
                                   firstName=self.first_name,
                                   lastName=self.last_name,
                                   role=self.role.role_name)

    class Meta:
        managed = False
        db_table = 'user_table'

class CategoryTable(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'category_table'

    def __str__(self):
        formatString = "{categoryId} : {categoryName}"
        return formatString.format(categoryId=self.category_id, categoryName=self.category_name)

class TicketTable(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    email = models.ForeignKey(UserTable, on_delete=models.CASCADE,db_column='email')
    category_id = models.ForeignKey(CategoryTable, on_delete=models.CASCADE,db_column='category_id')
    ticket_subject = models.CharField(max_length=45)
    ticket_description = models.CharField(max_length=255)
    creation_date = models.DateField()
    status = models.CharField(max_length=100)

    def __str__(self):
        formatString = "{ticketId} : {ticketSubject} : {ticketDescription} : {ticketStatus} : {email} : {name}"
        return formatString.format(ticketId=self.ticket_id, ticketSubject=self.ticket_subject, ticketDescription=self.ticket_description, ticketStatus=self.status, email=self.email.email, name=(self.email.first_name + " " + self.email.last_name))

    class Meta:
        managed = False
        db_table = 'ticket_table'

    def save(self,  *args, **kwargs):
        if not self.creation_date:
            today = timezone.now().today()
            today_str = today.strftime('%Y-%m-%d')
            self.data_of_reservation = today_str
        super().save(*args, **kwargs)
    
    


class AssignmentTable(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    ticket_id = models.ForeignKey('TicketTable', on_delete=models.CASCADE, db_column='ticket_id')
    email = models.ForeignKey('UserTable', on_delete=models.CASCADE, db_column='email')

    def __str__(self):
        stringZ = "{assignmentId}: {ticketId} : {email} : {name}"
        return stringZ.format(assignmentId=self.assignment_id,ticketId=self.ticket_id.ticket_id, email=self.email.email, name=(self.email.first_name + " " + self.email.last_name))

    class Meta:
        managed = False
        db_table = 'assignment_table'

class ActionTable(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    ticket_id = models.ForeignKey('TicketTable', on_delete=models.CASCADE, db_column='ticket_id')
    email = models.ForeignKey('UserTable', db_column='email', on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'ticket_table'


    def __str__(self):
        formatString = "{ActionId} : {ticketId} : {email} : {name}"
        return formatString.format(ActionId=self.assignment_id, item=self.tiket_id.ticket_id, email=self.email.email, name=(self.email.first_name + " " + self.email.last_name))
