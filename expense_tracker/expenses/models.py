from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Expense(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='expenses')
    expenseId = models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    category= models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)
    is_recurring = models.BooleanField(default=False)
    recurrence_period = models.CharField(
        max_length = 20,
        choices = [('daily','Daily'),('weekly','Weekly'),('monthly','Monthly'),('yearly','Yearly')],
        null=True,
        blank=True
    )
    next_due_date = models.DateField(null=True,blank=True)
    
    def __str__(self):
        return f"{self.title}  - {self.category}"

