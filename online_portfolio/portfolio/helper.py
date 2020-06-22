"""
helper functions for portfolio app
"""
from markdown import markdown
from django.utils.html import mark_safe
from .models import BasicInfo
from django.conf import settings


def as_markdown(content):
    return mark_safe(markdown(content, safe_mode="escape"))


def get_basic_info(user):
    basic_info = user.basicinfo
    default_info = BasicInfo.objects.get(pk=settings.DEFAULT_PORTFOLIO)

    def _get(key):
        real = getattr(basic_info, key)

        if real is None:
            return getattr(default_info, key)

        return real

    user_data = {
        "name": _get("name"),
        "phone1": _get("phone1"),
        "phone2": _get("phone2"),
        "about": _get("about"),
        "tag_line": _get("tag_line"),
        "call_of_contact": _get("call_of_contact"),
    }

    return user_data
