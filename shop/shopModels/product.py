from django.db import models
from authy.models import User, Address, Seller

import uuid
GENDER=(
    ('Male','Male'), ('Female','Female')
)
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE, related_name="subCategory")
    gender=models.CharField(max_length=10,choices=GENDER)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Sub-category'
        verbose_name_plural = 'Sub-categories'
    def __str__(self):
        return self.name+"->"+ self.gender
    

class Product(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True, editable=False)
    name = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey(Category, related_name='Product', on_delete=models.CASCADE)
    subcategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE, related_name="Product")
    desc = models.TextField()
    mrp = models.FloatField()
    price = models.FloatField()
    discount=models.FloatField()
    image = models.TextField()
    image2 = models.TextField(blank=True)
    brand=models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    seller=models.ForeignKey(Seller, related_name='seller',on_delete=models.CASCADE)

    class Meta:
        ordering = ('name','available')
        

    def __str__(self):
        return self.name


class ProductMedia(models.Model):
    media_link = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='imageSet')

    def __str__(self):
        return self.product__name


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviewUser', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='review', on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.TextField()
