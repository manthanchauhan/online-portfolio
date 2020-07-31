"""
forms for portfolio app
"""
from .models import BasicInfo, Project, Skill
from django.forms import ModelForm


class BasicInfoForm(ModelForm):
    class Meta:
        model = BasicInfo
        fields = ["name", "about", "tag_line", "profile_pic"]


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"


class AddSkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = "__all__"
