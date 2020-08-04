from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from .validators import all_space_validator
from django.conf import settings

# Create your models here.
class BasicInfo(models.Model):
    total_projects = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    name = models.CharField(
        default=settings.DEFAULT_BASIC_INFO["name"],
        max_length=40,
        validators=[all_space_validator],
    )
    email = models.EmailField(primary_key=True, max_length=50)
    phone1 = PhoneNumberField(null=True, blank=True)
    phone2 = PhoneNumberField(null=True, blank=True)
    about = models.CharField(
        default=settings.DEFAULT_BASIC_INFO["about"],
        max_length=2000,
        validators=[all_space_validator],
    )
    tag_line = models.CharField(
        default=settings.DEFAULT_BASIC_INFO["tag_line"], blank=True, max_length=55
    )
    call_of_contact = models.CharField(null=True, blank=True, max_length=400)
    profile_pic = models.CharField(
        max_length=200, default=settings.DEFAULT_BASIC_INFO["profile_pic"],
    )
    portfolio = models.CharField(null=True, blank=False, max_length=200)

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
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    user_profile = models.ForeignKey(
        BasicInfo, on_delete=models.CASCADE, editable=False
    )
    title = models.CharField(default=settings.DEFAULT_PROJECT["title"], max_length=50)
    description = models.CharField(
        default=settings.DEFAULT_PROJECT["description"], max_length=500
    )
    skills = models.CharField(
        default=settings.DEFAULT_PROJECT["skills"], max_length=100
    )
    live_link = models.CharField(blank=True, null=True, max_length=100)
    code_link = models.CharField(blank=True, null=True, max_length=100)
    image = models.CharField(max_length=200, default=settings.DEFAULT_PROJECT["image"],)

    class Meta:
        unique_together = (("user_profile", "title"), ("user_profile", "timestamp"))

    def update(self, data):
        self.__dict__.update(data)

    def to_dict(self):
        ans = {
            "serial_no": self.pk,
            "title": self.title,
            "timestamp": self.timestamp,
            "description": self.description,
            "skills": self.skills,
            "live_link": self.live_link,
            "code_link": self.code_link,
            "image": self.image,
        }
        return ans


class Skill(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    user_profile = models.ForeignKey(
        to=BasicInfo, on_delete=models.CASCADE, editable=True,
    )
    skill_name = models.CharField(
        max_length=40, default=settings.DEFAULT_SKILL["skill_name"]
    )
    category = models.CharField(
        max_length=50, default=settings.DEFAULT_SKILL["category"]
    )

    class Meta:
        unique_together = [("user_profile", "skill_name")]
