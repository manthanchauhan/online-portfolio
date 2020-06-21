"""
helper functions for portfolio app
"""
from markdown import markdown
from django.utils.html import mark_safe


def as_markdown(content):
    return mark_safe(markdown(content, safe_mode="escape"))
