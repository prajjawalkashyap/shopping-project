from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.text import slugify
# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_user(self,email,name,password,phone,**other_fields):
        email=self.normalize_email(email)
        user=self.model(email=email,name=name,phone=phone,**other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,name,password,phone,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        return self.create_user(email,name,password,phone,**other_fields)

class User(AbstractBaseUser,PermissionsMixin):

    email=models.EmailField(gettext_lazy('email address'),unique=True)
    name=models.CharField(max_length=150)
    phone=models.CharField(max_length=10)

    start_date=models.DateTimeField(default=timezone.now)
    is_active= models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects= CustomAccountManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['name','phone']

CHOICE=(
    ('Home','Home'),
    ('Work','Work'),
    ('Other','Other')
)

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='address')
    address=models.TextField()
    state=models.CharField(max_length=50)
    pin=models.CharField(max_length=6)
    type=models.CharField(max_length=100,choices=CHOICE)
    name=models.CharField(max_length=150)
    phone=models.CharField(max_length=10)


class Seller(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='seller')
    business_name=models.CharField(max_length=200)
    address1=models.TextField()
    pin1=models.PositiveIntegerField()
    address2=models.TextField()
    pin2=models.PositiveIntegerField()
    state=models.CharField(max_length=50)
    gst=models.CharField(max_length=50)
    accountNo=models.CharField(max_length=20)
    ifsc=models.CharField(max_length=50)

