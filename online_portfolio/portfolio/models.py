from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .validators import all_space_validator

# Create your models here.
class BasicInfo(models.Model):
    name = models.CharField(
        null=True, blank=True, max_length=40, validators=[all_space_validator]
    )
    email = models.EmailField(primary_key=True, max_length=50)
    phone1 = PhoneNumberField(null=True, blank=True)
    phone2 = PhoneNumberField(null=True, blank=True)
    about = models.CharField(
        null=True, blank=True, max_length=500, validators=[all_space_validator]
    )
    tag_line = models.CharField(null=True, blank=True, max_length=55)
    call_of_contact = models.CharField(null=True, blank=True, max_length=400)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profile_images/")

    def update(self, data):
        self.__dict__.update(data)
