"""
forms for portfolio app
"""
from .models import BasicInfo
from django.forms import ModelForm


class BasicInfoForm(ModelForm):
    class Meta:
        model = BasicInfo
        fields = "__all__"
