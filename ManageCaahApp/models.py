from django.db import models
from django.contrib.auth.models import  AbstractUser

class User(AbstractUser):

    def __str__(self):
        return f'{self.username}'

class AddCash(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_cash',
        null=True
    )
    source = models.CharField(max_length=100, null=True)
    datetime = models.DateTimeField(null=True)
    amount = models.FloatField(null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.user}'

class ExpenseModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_expanse',
        null=True
    )
    datetime = models.DateTimeField(null=True)
    amount = models.FloatField(null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.user}'