"""
helper functions for portfolio app
"""
from markdown import markdown
from django.utils.html import mark_safe
from .models import BasicInfo, Project
from django.conf import settings


def as_markdown(content):
    return mark_safe(markdown(content, safe_mode="escape"))


def get_basic_info(user):
    basic_info = user.basicinfo
    default_info = BasicInfo.objects.get(pk=settings.DEFAULT_USER)

    def _get(key):
        real = getattr(basic_info, key)

        if real is None:
            return getattr(default_info, key)

        return real

    user_data = {
        "name": _get("name"),
        "phone1": _get("phone1"),
        "phone2": _get("phone2"),
        "about": as_markdown(_get("about")),
        "tag_line": _get("tag_line"),
        "call_of_contact": _get("call_of_contact"),
        "profile_pic": basic_info.profile_pic,
        "portfolio": basic_info.portfolio,
    }

    return user_data


def get_projects_info(user):
    projects = Project.objects.filter(user_profile=user.basicinfo)

    result = []

    for project in projects:
        project_data = {
            "serial_no": project.pk,
            "timestamp": project.timestamp,
            "title": project.title,
            "description": as_markdown(project.description),
            "skills": project.skills,
            "live_link": project.live_link,
            "code_link": project.code_link,
            "image": project.image,
        }
        result.append(project_data)

    result.sort(key=lambda x: x["timestamp"])
    return result


def create_default_project(user):
    project = Project(user_profile=user.basicinfo)
    project.save()

    basic_info = user.basicinfo
    basic_info.total_projects += 1
    basic_info.save()
    return project
