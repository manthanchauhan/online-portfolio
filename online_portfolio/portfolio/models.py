from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField
from .validators import all_space_validator

# Create your models here.
class BasicInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        if "user" in data:
            raise Exception("cannot update user")

        self.__dict__.update(data)

    @staticmethod
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        """
        https://docs.djangoproject.com/en/3.0/ref/signals/#post-save
        :return: None
        """
        if created:
            BasicInfo.objects.create(user=instance, email=instance.email)


# class Project(models.Model)
