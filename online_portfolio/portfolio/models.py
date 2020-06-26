from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from .validators import all_space_validator

# Create your models here.
class BasicInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
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
    profile_pic = models.CharField(null=True, blank=False, max_length=200)

    def update(self, data):
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


class Project(models.Model):
    serial_no = models.IntegerField(validators=[MinValueValidator(0)], editable=False)
    user_profile = models.ForeignKey(
        BasicInfo, on_delete=models.CASCADE, editable=False
    )
    title = models.CharField(default="Project Title", max_length=50)
    description = models.CharField(default="Description", max_length=500)
    skills = models.CharField(default="Add skills here", max_length=100)
    live_link = models.CharField(blank=True, null=True, max_length=100)
    code_link = models.CharField(blank=True, null=True, max_length=100)
    image = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        unique_together = (("user_profile", "title"), ("user_profile", "serial_no"))

    def update(self, data):
        self.__dict__.update(data)
