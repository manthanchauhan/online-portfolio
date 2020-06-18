from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class BasicInfo(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField(primary_key=True, max_length=50)
    phone1 = PhoneNumberField(null=True)
    phone2 = PhoneNumberField(null=True)
    about = models.CharField(max_length=400)
    tag_line = models.CharField(max_length=55)
    call_of_contact = models.CharField(null=True, max_length=400)
    profile_pic = models.ImageField(null=True, upload_to="profile_images/")
