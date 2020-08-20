from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from book.models import Book


class ShopCart(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    quantity = models.IntegerField()

    def __str__(self):
        return self.title

    @property
    def stok_durum(self):
         return self.quantity



class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']
class Order(models.Model):
    STATUS =(
        ('New','New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    code= models.CharField(max_length=5,editable=False)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone = models.CharField(blank=True,max_length=25)
    address = models.CharField(blank=True,max_length=150)
    city = models.CharField(blank=True,max_length=50)
    country = models.CharField(blank=True,max_length=50)
    note = models.CharField(blank=True, max_length=250)
    total = models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote= models.CharField(blank=True,max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.first_name

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields=['first_name','last_name','address','phone','city','country']
        
        

class OrderBook(models.Model):
    STATUS =(
        ('New','New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    stok_durum = models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.book.title