from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField( null=True, blank=True)
    date = models.DateField()
   
    def __str__(self):
        return f"{self.user.username} - {self.amount}"  

class GroupExpense(models.Model):
    name = models.CharField(max_length=200)  
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    participants = models.ManyToManyField(User, related_name='group_expenses')  

    def split_amount(self):
        num_participants = self.participants.count()
        if num_participants > 0:
            return round(self.total_amount / num_participants, 2)
        return 0

    def __str__(self):
        return f"{self.name} - {self.total_amount}"