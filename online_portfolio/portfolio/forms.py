"""
forms for portfolio app
"""
from .models import BasicInfo, Project
from django.forms import ModelForm


class BasicInfoForm(ModelForm):
    class Meta:
        model = BasicInfo
        fields = ["name", "about", "tag_line", "profile_pic"]


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
