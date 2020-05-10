from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from food.models import Food


class ShopCart(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    @property
    def amount(self):
        return (self.quantity * self.product.price)

    @property
    def price(self):
        return (self.product.price)



class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']